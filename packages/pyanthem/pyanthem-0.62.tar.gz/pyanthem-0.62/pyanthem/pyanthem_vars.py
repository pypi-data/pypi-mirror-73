from os.path import realpath, join, split
self_fns = {
'fr':'entry',
'st_p':'entry',
'en_p':'entry',
'baseline':'entry',
'brightness':'entry',
'threshold':'entry',
'oct_add':'entry',
'scale_type':'entry',
'key':'entry',
'audio_format':'entry',
'Wshow':'entry',
'cmapchoice':'entry', 
'speed':'entry',
'file_in':'entry',
'file_out':'entry',
'save_path':'entry',
'Wshow_arr':'value'}

oct_add_opts = ['0','1','2','3','4','5']

scale_type_opts = ['Chromatic (12/oct)','Major scale (7/oct)','Minor scale (7/oct)', 
'Maj. triad (3/oct)','Min. triad (3/oct)','Aug. triad (3/oct)',
'Dim. triad (3/oct)','Maj. 6th (4/oct)','Min. 6th (4/oct)',
'Maj. 7th (4/oct)','Min. 7th (4/oct)','Aug. 7th (4/oct)',
'Dim. 7th (4/oct)','Maj. 7/9 (5/oct)','Min. 7/9 (5/oct)']

scaledata = [
[0,1,2,3,4,5,6,7,8,9,10,11],
[0,2,4,5,7,9,11],
[0,2,3,5,7,9,11],
[0,4,7],
[0,3,7],
[0,4,8],
[0,3,6],
[0,4,7,9 ],
[0,3,7,9 ],
[0,4,7,11],
[0,3,7,11],
[0,3,7,10],
[0,4,8,10],
[0,3,6,9 ],
[0,3,6,10],
[0,3,7,11],
[0,2,4,7,9,11],
[0,2,3,7,9,11]
]

key_opts = ['C','C#/D♭','D','D#/E♭','E','F','F#/G♭','G','G#/A♭','A','A#/B♭','B']

cmaps_opts = tuple(sorted(['viridis', 'plasma', 'inferno', 'magma', 'cividis','binary', 
'bone', 'pink','spring', 'summer', 'autumn', 'winter', 'cool','hot','copper','Spectral', 
'coolwarm', 'bwr', 'seismic','twilight', 'hsv', 'Paired', 'prism', 'ocean', 
'terrain','brg', 'rainbow', 'jet'],key=lambda s: s.lower()))

pth=split(realpath(__file__))[0]
example_files_decomp = [join(pth,'anthem_datasets',d) for d in ['demo1.mat','demo2.mat','demo3.mat','demo4.mat']]
example_files_raw = [join(pth,'anthem_datasets',d) for d in ['raw1.mat','raw2.mat']]
example_cfg = [join(pth,'anthem_datasets',d) for d in ['demo1_cfg.p','demo2_cfg.p','demo3_cfg.p','demo4_cfg.p']]

soundfonts={
'piano_small':'12WYF3pc_kYI5myMjgEUnb-y2CeX3fucx',
'piano_large':'1DEKLuSiJ4QsHdipfzQdKGsmFn5_4ipOL',
'e-piano':'0B4_6p-MMrzwLeTBfNzl1SmVVSEU',
'strings':'1c0pCI0YdcFEpSLEbCW8HTzFOlJpz0HS9'
}




