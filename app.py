import streamlit as st
import nltk
from collections import defaultdict
from nltk.util import ngrams

st.set_page_config(page_title="AI Autofill", page_icon="📝")

@st.cache_resource
def load_model():
    nltk.download('gutenberg', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    raw_text = nltk.corpus.gutenberg.raw('austen-emma.txt')
    tokens = [w.lower() for w in nltk.word_tokenize(raw_text) if w.isalpha()]
    
    model = defaultdict(lambda: defaultdict(lambda: 0))
    for w1, w2, w3 in ngrams(tokens, 3):
        model[(w1, w2)][w3] += 1
    
    for context in model:
        total = sum(model[context].values())
        for w3 in model[context]:
            model[context][w3] /= total
    return model

model = load_model()

st.title("🚀 Smart Autofill System")
if 'text' not in st.session_state:
    st.session_state.text = ""

input_text = st.text_input("اكتب جملة:", value=st.session_state.text)

if input_text:
    words = input_text.lower().split()
    if len(words) >= 2:
        context = (words[-2], words[-1])
        if context in model:
            suggestions = sorted(model[context].items(), key=lambda x: x[1], reverse=True)[:3]
            st.write("### الكلمات المقترحة:")
            cols = st.columns(3)
            for i, (word, prob) in enumerate(suggestions):
                if cols[i].button(word.capitalize()):
                    st.session_state.text = input_text + " " + word
                    st.rerun()
        else:
            st.warning("لا توجد اقتراحات لهذا السياق.")