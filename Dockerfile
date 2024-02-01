FROM debian:bookworm-slim

WORKDIR /usr/app/

# 依存関係のインストール
RUN apt-get update -qq \
    && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# ドキュメントのダウンロード
RUN git clone --filter=blob:none --sparse https://github.com/elastic/built-docs.git \
    && cd built-docs \
    && git sparse-checkout set ./raw/en/elasticsearch/reference/current

# ドキュメントのみをコピー
RUN mkdir -p /usr/app/src/assets
CMD cp ./built-docs/raw/en/elasticsearch/reference/current/*.html /usr/app/src/assets/

