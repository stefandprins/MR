# import sys
# import os
# import django

# # Add project root to Python path
# sys.path.append('/mnt/c/Users/dev/Desktop/MRS')

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
# django.setup()


import numpy as np
from tables import open_file
from api.models import Song  # your model
from api.utils.hdf5_getters import *
from api.utils.utils import get_all_files
from django.db.models import Avg

# data_folder = '/../../MillionSongSubset'
# data_folder = '/mnt/c/Users/dev/Desktop/MRS/MillionSongSubset'

def safe_mean(array):
    return float(np.mean(array)) if array is not None and len(array) > 0 else None

def collect_and_store(data_folder):
    files = get_all_files(data_folder)
    
    songs_to_create = []

    existing_ids = set(Song.objects.values_list('track_id', flat=True))

    for path in files:
        try:
            h5 = open_file(path, mode='r')
            track_id = get_track_id(h5).decode('utf-8')
            if track_id in existing_ids:
                # print(f"Skipping existing tracks.")
                h5.close()
                continue
            # if Song.objects.filter(track_id=track_id).exists():
            #     # pr int(f"Skipping {track_id}: already exists.")
            #     h5.close()
            #     continue

            try:
                artist_familiarity = get_artist_familiarity(h5)
            except:
                artist_familiarity = None

            # Raw arrays
            segments_pitches = get_segments_pitches(h5)  # (N, 12)
            segments_timbre = get_segments_timbre(h5)   # (N, 12)
            segments_start = get_segments_start(h5)
            beats_start = get_beats_start(h5)
            bars_start = get_bars_start(h5)

            # Summarized content features
            avg_pitch = np.mean(segments_pitches, axis=0).tolist()
            avg_timbre = np.mean(segments_timbre, axis=0).tolist()

            # Timing-based features
            mean_beat_interval = float(np.mean(np.diff(beats_start))) if len(beats_start) > 1 else None
            mean_bar_interval = float(np.mean(np.diff(bars_start))) if len(bars_start) > 1 else None
            segment_density = len(segments_start) / get_duration(h5) if get_duration(h5) > 0 else None

            avg_loudness_max = safe_mean(get_segments_loudness_max(h5))
            avg_loudness_start = safe_mean(get_segments_loudness_start(h5))
            avg_confidence = safe_mean(get_segments_confidence(h5))
            avg_beat_confidence = safe_mean(get_beats_confidence(h5))

            terms = get_artist_terms(h5)
            weights = get_artist_terms_weight(h5)

            # Get the index of the highest-weighted term
            # top_index = np.argmax(weights)

            # Decode and assign the single top term
            # artist_term = terms[top_index].decode('utf-8')

            if len(terms) > 0 and len(weights) > 0:
                top_index = np.argmax(weights)
                artist_term = terms[top_index].decode('utf-8')
            else:
                artist_term = None  # Or set a default string like "unknown"


            
            song = Song(
                artist_name=get_artist_name(h5).decode('utf-8'),
                title=get_title(h5).decode('utf-8'),
                duration=get_duration(h5),
                year=get_year(h5),
                artist_familiarity=artist_familiarity,
                tempo=get_tempo(h5),
                key=get_key(h5),
                mode=get_mode(h5),
                track_id=get_track_id(h5).decode('utf-8'),

                # Audio features specifically for CBF
                loudness = get_loudness(h5),
                time_signature = get_time_signature(h5),
                mean_beat_interval=mean_beat_interval,
                mean_bar_interval=mean_bar_interval,
                segment_density=segment_density,
                avg_loudness_max=avg_loudness_max,
                avg_loudness_start=avg_loudness_start,
                segment_confidence=avg_confidence,
                beat_confidence=avg_beat_confidence,
                artist_term = artist_term,
            )

            for i in range(12):
                    setattr(song, f"avg_pitch_{i}", avg_pitch[i])
                    setattr(song, f"avg_timbre_{i}", avg_timbre[i])
            songs_to_create.append(song)
            h5.close()
        except Exception as e:
            print(f"Error processing {path}: {e}")
            
        finally:
            if h5 is not None:
                h5.close()

    # ✅ Bulk insert here
    if songs_to_create:
        Song.objects.bulk_create(songs_to_create, batch_size=500)
        print(f"✅ Inserted {len(songs_to_create)} new songs.")

def replace_none_with_avg():
    print("🧹 Filling missing scalar fields with column-wise averages...")

    scalar_fields = [
        'avg_loudness_max', 'avg_loudness_start',
        'segment_confidence', 'beat_confidence',
        'mean_beat_interval', 'mean_bar_interval',
        'segment_density'
    ]

    averages = {}
    for field in scalar_fields:
        avg_value = Song.objects.filter(**{f"{field}__isnull": False}).aggregate(avg=Avg(field))['avg']
        if avg_value is not None:
            averages[field] = float(avg_value)
            print(f"→ Average {field}: {averages[field]:.4f}")
        else:
            print(f"⚠️ No values for {field}")

    updated = 0
    for song in Song.objects.all():
        changed = False
        for field, avg in averages.items():
            if getattr(song, field) is None:
                setattr(song, field, avg)
                changed = True
        if changed:
            song.save()
            updated += 1

    print(f"\n✅ Updated {updated} songs with fallback averages.")

