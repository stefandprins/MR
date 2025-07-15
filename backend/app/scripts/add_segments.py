from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.database import SessionLocal
from app.db.models import Segment, Track
from app.utils.hdf5_files import get_all_files
from app.utils.hdf5_getters import *
from tables import open_file

# data_folder = '/mnt/c/Users/dev/Desktop/MRS/MillionSongSubset'
data_folder = '/mnt/c/Users/dev/Desktop/MRS/MillionSong'
BATCH_SIZE = 10

def add_segments():
    files = get_all_files(data_folder)
    db: Session = SessionLocal()

    track_lookup = {track.track_id: track.id for track in db.execute(select(Track.id, Track.track_id)).all()}

    batch = []
    total_added = 0

    for i, path in enumerate(files, 1):
        h5 = None
        try:
            h5 = open_file(path, mode='r')
            track_id_str = get_track_id(h5).decode('utf-8')
            track_db_id = track_lookup.get(track_id_str)

            if not track_db_id:
                print(f"Track not found in DB: {track_id_str}")
                continue

            loudness_max = get_segments_loudness_max(h5)
            confidence = get_segments_confidence(h5)
            pitch = get_segments_pitches(h5)
            timbre = get_segments_timbre(h5)

            segments = []
            for idx in range(len(confidence)):
                segment = {
                    "segment_index": int(idx),
                    "pitch": [float(p) for p in pitch[idx]],
                    "timbre": [float(t) for t in timbre[idx]],
                    "loudness_max": float(loudness_max[idx]),
                    "confidence": float(confidence[idx]),
                }
                segments.append(segment)

            batch.append(Segment(track_id=track_db_id, segments=segments))

        except Exception as e:
            print(f"Error reading {path}: {e}")
        finally:
            if h5:
                h5.close()

        # Process batch
        if len(batch) >= BATCH_SIZE:
            db.bulk_save_objects(batch)
            db.commit()
            total_added += len(batch)
            batch.clear()
            print(f"Inserted batch, total so far: {total_added}")

        if i % 1000 == 0:
            print(f"Processed {i}/{len(files)} files...")

    # Final commit for leftovers
    if batch:
        db.bulk_save_objects(batch)
        db.commit()
        total_added += len(batch)
        print(f"Inserted final batch. Total inserted: {total_added}")

    db.close()
    print(f"Done: {total_added} segment records added.")

if __name__ == "__main__":
    add_segments()