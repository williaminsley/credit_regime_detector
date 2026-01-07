from src.data_loader import DownloadConfig, download_adj_close


def main() -> None:
    cfg = DownloadConfig()
    prices = download_adj_close(cfg)
    print(prices.tail())


if __name__ == "__main__":
    main()
