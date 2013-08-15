#!/usr/bin/env python2
# zipfsong: Get the best songs assuming the Zipfian distribution.

import sys

class Song:
    def __init__(self, name, plays, song_no):
        self.name = name
        self.plays = plays
        self.song_no = song_no

    def __str__(self):
        return self.name

def read_input():
    songs = list()
    num_songs, num_select = [int(num) for num in sys.stdin.readline().split()]
    for i in range(1, num_songs + 1):
        plays, name = sys.stdin.readline().split()
        songs.append(Song(name, int(plays), i))
    return (songs, num_select)

def total_nbr_plays(songs):
    return sum([song.plays for song in songs])

def calc_quality(songs, total_plays):
    z_1 = total_plays / sum([float(1)/i for i in range(1, len(songs) + 1)])
    for song in songs:
        if z_1 > 0:
            song.quality = song.plays * song.song_no / z_1
        else:
            song.quality = 0

def get_best(songs, num_select):
    songs_sorted = sorted(songs, reverse = True, key= lambda o: (o.quality, -o.song_no))
    return songs_sorted[:num_select]

def main():
    songs, num_select = read_input()
    if len(songs) > 0:
        total_plays = total_nbr_plays(songs)
        calc_quality(songs, total_plays)
        best_songs = get_best(songs, num_select)
        for quality_song in best_songs:
            print(quality_song)

if __name__ == "__main__":
    main()
