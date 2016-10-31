from __spider__.douban import get_movie_ids, handle_one_movie


if __name__ == '__main__':
    ids = get_movie_ids()   # get all the ids
    print len(ids)
    for movie_id in ids:    # handle the ids one by one
        handle_one_movie(movie_id)
