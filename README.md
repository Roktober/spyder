# Spyder

### Description
Service for page parsing
### CLI
#### Command list
##### get
```
Usage: main.py get [OPTIONS] URL

  load URL TITLE from storage

Options:
  --limit INTEGER  Number of load rows.  [default: 10]
  --help           Show this message and exit.
```

##### load
```
Usage: main.py load [OPTIONS] URL

  load html recursive

Options:
  --depth INTEGER  Parsing depth.  [default: 2]
  --help           Show this message and exit.

```
Example:

```
python main.py load http://www.vesti.ru/ --depth 2
ok, execution time: 65s, peak memory usage: 217 Mb
python main.py get http://www.vesti.ru/ --limit 2
http://www.vesti.ru/news/ Вести.Ru: новости, видео и фото дня
http://www.vestifinance.ru/ Вести Экономика: Главные события российской и мировой экономики, деловые новости,  фондовый рынок
```

### Installation and run
```bash
git clone ...
make build
ocker-compose up -d
docker-compose run --rm app python /app/src/main.py COMMAND URL OPTIONS
```
