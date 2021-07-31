from CLI import CLI


def main():
    cli: CLI = CLI()
    print(cli.get_jwt_token())


if __name__ == "__main__":
    main()
