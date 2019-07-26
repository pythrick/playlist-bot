from instagram import get_comments


def write_to_file(values):
    with open('database.csv', 'w') as file:
        for line in values:
            file.write('"{}"\n'.format(line))


if __name__ == '__main__':
    comments = get_comments()
    write_to_file(comments)
