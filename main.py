from services.instagram import InstagramService


def write_to_file(values):
    with open('database.csv', 'w') as file:
        for line in values:
            file.write('"{}"\n'.format(line))


if __name__ == '__main__':
    instagram_service = InstagramService()
    comments = instagram_service.list_comments()
    write_to_file(comments)
