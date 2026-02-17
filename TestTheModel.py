import Model
from Dataset import VOCAB, training_loader, validation_loader, test_loader
import torch
from torch import nn

device = "cpu"
model = Model.SyntaxClassifier(len(VOCAB))
model.load_state_dict(torch.load("syntax_model.pth", map_location=device))
criterion = nn.BCEWithLogitsLoss()

model.eval()

print("Test results")
val_loss, val_acc = Model.evaluate(model, test_loader, criterion)
print(
    f"Test Loss: {val_loss:.4f} | "
    f"Test Acc: {val_acc:.4f}"
)