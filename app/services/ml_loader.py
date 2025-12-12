from transformers import (
  pipeline,
  AutoTokenizer,
  AutoModelForSequenceClassification,
  AutoModelForCausalLM,
  AutoModelForSeq2SeqLM
)
import torch
import threading

class MLModels:
  intent_classifier = None
  sentiment_classifier = None
  summarizer = None
  dialog_model = None
  dialog_tokenizer = None
  _lock = threading.Lock()

def load_models():
  """
  Load all pretrained models at startup.
  This runs ONCE when Uvicorn boots.
  """

  print("Loading ML models...")

  with MLModels._lock:
    if MLModels.intent_classifier is not None:
      print("ML models already loaded — skipping reload.")
      return

    print("\n========== LOADING ML MODELS ==========\n")

    device = 0 if torch.cuda.is_available() else -1
    print(f"Using device: {'GPU' if device == 0 else 'CPU'}")

    # -------- Intent Classification (mDeBERTa MNLI) --------
    MLModels.intent_classifier = pipeline(
      "zero-shot-classification",
      model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
      device=device
    )
    print("✓ Intent classifier loaded")

    # -------- Sentiment Analysis (DistilBERT) --------
    MLModels.sentiment_classifier = pipeline(
      "sentiment-analysis",
      model="distilbert-base-uncased-finetuned-sst-2-english",
      device=device
    )
    print("✓ Sentiment classifier loaded")

    # -------- Summarization (FLAN-T5 Small) --------
    MLModels.summarizer = pipeline(
      "text2text-generation",
      model="google/flan-t5-small",
      device=device
    )
    print("✓ Summarizer loaded")

    # -------- Conversational Model (DialoGPT Medium) --------
    MLModels.dialog_tokenizer = AutoTokenizer.from_pretrained(
      "microsoft/DialoGPT-medium"
    )
    MLModels.dialog_model = AutoModelForCausalLM.from_pretrained(
      "microsoft/DialoGPT-medium"
    ).to("cuda" if device == 0 else "cpu")

    print("✓ Conversational model loaded")
    print("\n========== ALL MODELS READY ==========\n")

  # #--- Intent Classification (BART-MNLI) ---
  # MLModels.intent_classifier = pipeline(
  #   "zero-shot-classification",
  #   model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
  # )

  # #--- Sentiment Analysis ---
  # MLModels.sentiment_classifier = pipeline(
  #   "sentiment-analysis",
  #   model="distilbert-base-uncased-finetuned-sst-2-english"
  # )

  # #--- Summarization (FLAN-T5) ---
  # MLModels.summarizer = pipeline(
  #   "text2text-generation",
  #   model="google/flan-t5-small"
  # )

  # # --- Conversational Model (DialoGPT) ---
  # MLModels.dialog_tokenizer = AutoTokenizer.from_pretrained(
  #   "microsoft/DialoGPT-medium"
  # )
  # MLModels.dialog_model = AutoModelForCausalLM.from_pretrained(
  #   "microsoft/DialoGPT-medium"
  # )

  # print("All ML models loaded successfully!")

def get_intent_classifier():
  return MLModels.intent_classifier

def get_sentiment_classifier():
  return MLModels.sentiment_classifier

def get_summarizer():
  return MLModels.summarizer

def get_dialog_model():
  return MLModels.dialog_model, MLModels.dialog_tokenizer

