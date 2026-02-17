import torch
import torch.nn as nn
import Dataset
from Dataset import VOCAB, training_loader, validation_loader, test_loader

class SyntaxClassifier(nn.Module):
    def __init__(
            self,
            vocab_size: int,
            embedding_dim: int = 128,
            hidden_dim: int = 256,
            num_layers: int = 2,
            dropout: float = 0.3
    ):
        super().__init__()

        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=embedding_dim,
            padding_idx=0  # assuming <PAD> = 0
        )

        self.lstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0.0
        )

        self.fc = nn.Linear(hidden_dim * 2, 1)  # *2 for bidirectional
        self.dropout = nn.Dropout(dropout)

    def forward(self, input_ids, attention_mask=None):
        """
        input_ids: (batch_size, seq_len)
        attention_mask: (batch_size, seq_len) with 1 = real token, 0 = padding
        """

        x = self.embedding(input_ids)
        # x shape: (batch_size, seq_len, embedding_dim)

        lstm_out, _ = self.lstm(x)
        # lstm_out shape: (batch_size, seq_len, hidden_dim * 2)

        if attention_mask is not None:
            mask = attention_mask.unsqueeze(-1)  # (batch_size, seq_len, 1)
            lstm_out = lstm_out * mask

            # Mean pooling over valid tokens
            summed = torch.sum(lstm_out, dim=1)
            counts = torch.clamp(mask.sum(dim=1), min=1e-9)
            pooled = summed / counts
        else:
            # Simple mean pooling if no mask
            pooled = lstm_out.mean(dim=1)

        pooled = self.dropout(pooled)
        logits = self.fc(pooled)

        return logits.squeeze(-1)

device = "cpu"

def train_one_epoch(model, dataloader, optimizer, criterion):
    model.train()
    total_loss = 0.0

    for batch in dataloader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        optimizer.zero_grad()

        logits = model(input_ids, attention_mask)
        loss = criterion(logits, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(dataloader)

def evaluate(model, dataloader, criterion):
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            logits = model(input_ids, attention_mask)
            labels = labels.float()
            loss = criterion(logits, labels)
            total_loss += loss.item()

            preds = torch.sigmoid(logits) > 0.5
            correct += (preds == labels.bool()).sum().item()
            total += labels.size(0)

    accuracy = correct / total
    return total_loss / len(dataloader), accuracy

if __name__ == "__main__":
    model = SyntaxClassifier(vocab_size=len(VOCAB)).to("cpu")
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    num_epochs = 10

    for epoch in range(num_epochs):
        train_loss = train_one_epoch(
            model,
            training_loader,
            optimizer,
            criterion
        )

        val_loss, val_acc = evaluate(
            model,
            validation_loader,
            criterion
        )

        print(
            f"Epoch {epoch+1}/{num_epochs} | "
            f"Train Loss: {train_loss:.4f} | "
            f"Val Loss: {val_loss:.4f} | "
            f"Val Acc: {val_acc:.4f}"
        )

    torch.save(model.state_dict(), "syntax_model.pth")

