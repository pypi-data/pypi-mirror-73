from .model import TextRank, GPT2ForQuestionGeneration
from .util import SentencePreprocessor, PDFProcessor
from tqdm import tqdm

class Generator(object):
    def __init__(self, pdf_path, translate_api_url, translate_api_port, gpt2_api_url, gpt2_api_port):
        self.pdf = PDFProcessor(pdf_path)
        self.text = self.pdf.get_pdf_text()
        self.sumarization_model = TextRank(n_word=5, word_min_len=2, sentence_min_len=6)
        self.preprocessor = SentencePreprocessor(api_url=translate_api_url, api_port=translate_api_port)
        self.gpt2 = GPT2ForQuestionGeneration(api_url=gpt2_api_url, api_port=gpt2_api_port)

    def summarize(self):
        print('=====Start Summarization=====')
        kw_list = self.sumarization_model.get_keywords(self.text)
        important_sentece = self.sumarization_model.get_key_sentences(kw_list, self.text)
        print('=====Summarization finished=====')
        return list(important_sentece.keys())
    
    def filt(self, sentence_list):
        regular_sentence = []
        print('=====Start filter=====')
        pbar = tqdm(sentence_list)
        for index, sentence in enumerate(pbar):
            pbar.set_description("Processing sentence %s" % index)
            if self.preprocessor.is_sentence(sentence):
                regular_sentence.append(sentence)
            else:
                pass
        print('=====Filter finished=====')
        return regular_sentence
    
    def translate(self, regular_sentence_list):
        eng_sentence = []
        print('=====Start Translation=====')
        pbar = tqdm(regular_sentence_list)
        for index, sentence in enumerate(pbar):
            pbar.set_description("Processing sentence %s" % index)
            tgt_sentence = self.preprocessor.translateToEnglish(sentence)
            eng_sentence.append(tgt_sentence)
        print('=====Translation finished=====')
        return eng_sentence

    def generate_guestion(self, regular_sentence_list):
        qa_list = []
        print('=====Start generation=====')
        eng_sentences = self.translate(regular_sentence_list)
        questions = self.gpt2.generate(eng_sentences)
        for q, a in zip(questions, regular_sentence_list):
            qa_list.append((q, a))
        print('=====Generation finished=====')
        return qa_list
    
    def get_qa(self):
        important_senteces = self.summarize()
        regular_sentences = self.filt(important_senteces)
        qas = self.generate_guestion(regular_sentences)
        return qas