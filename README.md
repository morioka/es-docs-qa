# es-docs-qa

ベクトルデータベースとしてElasticsearchをつかう、RetrievalQA chatbot を作ってみる記事、"[ChatGPT+LangChain| Elasticsearch公式ドキュメントのQ&Aを作ってみる](https://zenn.dev/zozotech/articles/86543f2ad9a09e)"を再現する。

- 記事中にコード断片はあるが、欠けている部分を補う。
- langchainのAPI変更で、整合しないところがあったので修正


## 実行

```bash
# elasticsearch-kibanaコンテナを作成。サンプルデータをダウンロード
$ docker compose up -d --build

# インデックスを生成
$ python src/setting.py
# chatbotを実行
$ python src/main.py
```

