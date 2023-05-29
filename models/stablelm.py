from transformers import AutoModelForCausalLM, AutoTokenizer
from optimum.bettertransformer import BetterTransformer

def load_model(base, finetuned, multi_gpu, force_download_ckpt):
    tokenizer = AutoTokenizer.from_pretrained(base)
    tokenizer.pad_token_id = 1
    tokenizer.eos_token_id = 0
    tokenizer.padding_side = "left"

    model = AutoModelForCausalLM.from_pretrained(
        base, 
        load_in_8bit=False if multi_gpu else True, 
        device_map="auto")

    if multi_gpu:
        model.half()

    model = BetterTransformer.transform(model)
    return model, tokenizer