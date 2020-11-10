from lexrankr import LexRank
from transformers import *
from summarizer import Summarizer
import pickle

class Summarize:
    def __init__(self, paragraph, num):
        try:
            if isinstance(paragraph, str) is True:
                self.paragraph = paragraph
                self.probe_num = num
        except AttributeError as e:
            raise TypeError("You can't use it if it is not string.")

    def summarize(self):
        lex = LexRank()
        lex.summarize(self.paragraph)
        summaries = lex.probe(self.probe_num)
        return summaries

    def bertSum(self):
        # Load model, model config and tokenizer via Transformers
        with open('/home/lab05/A1B4/wow/static/kcbert_large/kcbert_base_config.bin', 'rb') as f:
            custom_config = pickle.load(f)
        custom_config.output_hidden_states=True
        with open('/home/lab05/A1B4/wow/static/kcbert_large/kcbert_base_tokenizer.bin', 'rb') as f:
            custom_tokenizer = pickle.load(f)
        # custom_tokenizer = AutoTokenizer.from_pretrained('beomi/kcbert-base')
        # with open('/home/lab05/A1B4/wow/static/kcbert_large/kcbert_base_model.bin', 'rb') as f:
        #     custom_model = pickle.load(f)
        custom_model = AutoModel.from_pretrained('beomi/kcbert-base', config=custom_config)
        summarizer_model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)
        summaries = summarizer_model(self.paragraph, num_sentences=self.probe_num)
        return summaries