#Author: Judy Fong <lvl@judyyfong.xyz.> Reykjavik University
#Description:

def main():
    #write code here
    import csv

    episodes = list(csv.reader(open('data/studentSignUpSheet.tsv', 'r'),
    delimiter='\t'))
    # remove the signup header
    episodes.pop(0)
    correctedEpisodes = []
    for episode in episodes:
        if episode[2] or episode[1]:
            print(episode[0])
if __name__ == '__main__':
    main()
