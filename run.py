import numpy as np
from thinkdsp import read_wave, Impulses, CosSignal, Wave
import streamlit as st

def normal(audio_bytes):
    st.audio(audio_bytes, format="audio/wav")

st.title("Audo Definition Metadata")

uploaded_file = st.file_uploader("Upload WAV file", type="wav")

if uploaded_file is not None:
    st.write("Original Waveform:")
    normal_wave = read_wave(uploaded_file)
    normal_wave.normalize()
    normal(uploaded_file)
    
    st.write('Choose an option:')
    option = st.radio('', ['Impulses', 'CosSignal', 'Wave'])
    
    if option == 'Impulses':
        st.write("Impulses Applied:")
        imp_sig = Impulses([0.005, 0.3, 0.6, 0.9], amps=[1, 0.5, 0.25, 0.1])
        impulses_wave = imp_sig.make_wave(start=0, duration=normal_wave.duration, framerate=normal_wave.framerate)
        convolved = normal_wave.convolve(impulses_wave)
        
        convolved.write('temp.wav')
        st.audio(open('temp.wav', 'rb'), format="audio/wav")

    elif option == 'CosSignal':
        n = st.number_input('Enter the frequency')
        carrier_sig = CosSignal(freq=n)
        carrier_wave = carrier_sig.make_wave(duration=normal_wave.duration, framerate=normal_wave.framerate)
        modulated = normal_wave * carrier_wave

        modulated.write('temp.wav')
        st.audio(open('temp.wav', 'rb'), format="audio/wav")

    elif option == 'Wave':
        factor = st.number_input('Enter the factor', step=1.0, min_value=1.0)
        factor = int(factor)
        ys = np.zeros(len(normal_wave))
        ys[::factor] = normal_wave.ys[::factor]
        sampled = Wave(ys, framerate=normal_wave.framerate)

        sampled.write('temp.wav')
        st.audio(open('temp.wav', 'rb'), format="audio/wav")
