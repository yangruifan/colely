import logging
import fire
from tao_piao_piao.spider import run_tpp_spider


class Spider:
    def __init__(self):
        run_tpp_spider()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(Spider)
