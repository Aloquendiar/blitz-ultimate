import mido
import os
from mido import MidiFile, MidiTrack

def process_folder(root_directory):
    allowed_tracks = {
        "PART BASS", "PART GUITAR", "PART DRUMS", 
        "PART KEYS", "PART VOCALS", "HARM1", "HARM2", "HARM3"
    }

    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.lower().endswith(('.mid', '.midi')):
                file_path = os.path.join(root, file)
                
                try:
                    mid = MidiFile(file_path)
                    
                    # 1. Validación de pistas
                    has_target_tracks = False
                    for track in mid.tracks:
                        for msg in track:
                            if msg.type == 'track_name' and msg.name.strip().upper() in allowed_tracks:
                                has_target_tracks = True
                                break
                        if has_target_tracks: break
                    
                    if not has_target_tracks:
                        continue

                    # 2. Configuración del nuevo MIDI
                    new_mid = MidiFile(ticks_per_beat=480)
                    # Calculamos el factor con alta precisión
                    scale_factor = 480.0 / mid.ticks_per_beat

                    for track in mid.tracks:
                        new_track = MidiTrack()
                        keep_track = False
                        
                        # Comprobar si esta pista específica es una de las permitidas o la de tempo
                        is_tempo_track = any(msg.type in ['set_tempo', 'time_signature'] for msg in track)
                        is_named_track = any(msg.type == 'track_name' and msg.name.strip().upper() in allowed_tracks for msg in track)

                        if is_tempo_track or is_named_track:
                            for msg in track:
                                # Escalado preciso del delta time
                                # Usamos round para evitar que pequeños errores de flotante muevan la nota
                                new_time = int(round(msg.time * scale_factor))
                                
                                # Copiamos el mensaje con el nuevo tiempo escalado
                                new_msg = msg.copy(time=new_time)
                                new_track.append(new_msg)
                            
                            new_mid.tracks.append(new_track)

                    # 3. Guardar manteniendo el nombre y ruta
                    new_mid.save(file_path)
                    print(f"PROCESADO (Offset preservado): {file_path}")

                except Exception as e:
                    print(f"Error en {file_path}: {e}")

if __name__ == "__main__":
    # Asegúrate de poner la ruta correcta aquí
    process_folder("Z:\\Documentos\\GitHub\\blitz-ultimate\\_ark\\songs\\updates")