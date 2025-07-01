from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TDRC
from src import FileManipulationVariables


def set_mp3_covers(
        mp3_directory_path: str, 
        cover_path: str, 
        mime: str,
        year: str
        ):
    # get .mp3 files under directory
    mp3_dir_path = Path(mp3_directory_path)
    mp3_files = []
    for my_path in mp3_dir_path.iterdir():
        if my_path.is_file() and my_path.name.endswith('.mp3'):
            mp3_files.append(my_path)
    
    # set cover art for mp3 files
    for my_mp3_file in mp3_files:
        set_one_cover(
            mp3_path=my_mp3_file, 
            cover_path=cover_path,
            mime=mime,
            year=year
            )


def set_one_cover(mp3_path: Path, cover_path: str, mime: str, year: str):
    # parse image
    with open(cover_path, 'rb') as f:
        image_data = f.read()

    # try to open the mp3 file
    try:
        audio = MP3(mp3_path, ID3=ID3)

        # If there's no ID3 tag, add one
        if audio.tags is None:
            audio.add_tags()
        else:
            # Remove existing APIC (cover art) frames
            audio.tags.delall('APIC')

        # add or replace the album art
        audio.tags.add(
            APIC(
                encoding=3, # 3 is for UTF-8
                mime=mime, # MIME type (image/jpeg or image/png),
                type=3, # 3 is for front cover
                desc=u'Cover',
                data=image_data
            )
        )

        if year:
            audio.tags.add(TDRC(encoding=3, text=year))
        
        # save
        audio.save()

    except Exception as e:
        print(f'[+] Error: {e}')
