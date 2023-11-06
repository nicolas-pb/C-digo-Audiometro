#Prueba aleatoria 

import numpy as np
import sounddevice as sd #Para escuchar el audio de un vector
#import soundfile as sf
#import time

SAMPLE_RATE = 44100
AUDIOMETRIC_FREQS = np.array([125, 250, 500, 1000, 2000, 4000, 8000])
AUDIOMETRIC_FREQS_EXT = np.array([63, 3000, 6000, 12000, 14000, 16000])

EARS_VALUES = {
    "left": 0,
    "right": 1    
}

ORDER_FREQS = [3,4,5,6,0,1,2,3]

def frequency_run(ear, frequency, time_array, power_gains):
    
    tone = np.sin(2 * np.pi * frequency * time_array)
    
    level_idx = 0
    
    while True:
        weighted_tone = power_gains[level_idx] * tone #Tono ponderaro
        
        if EARS_VALUES[ear]:
            stereo_tone = np.vstack((np.zeros_like(weighted_tone), weighted_tone))
        else:
            stereo_tone = np.vstack((weighted_tone, np.zeros_like(weighted_tone)))
            
        sd.play(stereo_tone.T, SAMPLE_RATE)
        
        response = int(input("Did you ear the tone? \n Yes: 1 ; No: 0 \n"))
        
        if bool(response):
            level_idx += 1
        else:
            break
        
    return level_idx
        
def main(RETD, RETA, audio_secs, ear):
    time_array = np.arange(SAMPLE_RATE * audio_secs) / SAMPLE_RATE #Vector tiempo
    
    gain_steps = np.linspace(RETA-1, RETD+4, (RETD - RETA + 6))
    
    power_gains = (1/(2**gain_steps)) #Resolución de los pasos
   
    
    results = []
    for freq_i in AUDIOMETRIC_FREQS[ORDER_FREQS]:
        level_idx = frequency_run(ear, freq_i, time_array, power_gains)
        print(f"{freq_i} Hz: {20*np.log10(power_gains[level_idx])}")
        results.append((freq_i,level_idx))
#        print(results)
    return results

if __name__ == "__main__":    
    RETD = [(1000, 12),(2000, 13),(4000, 11),(8000, 7),(125, 8),(250, 8),(500, 9),(1000, 12)]
    RETA = 7
    audio_secs = 1
    ear = "right"
    RETDD = main(RETD, RETA, audio_secs, ear)
    RETDA = main(RETD, RETA, audio_secs, ear)
    