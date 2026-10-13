# Solana Path

This is for decision-making and planning within the Solana ecosystem in cambrian. 

## Current
We have 2 servers running in pinax connected firehose which has data redundancy problems like missing inner function calls. Also latency when the network is too busy.
On the other side we implemented an initial version of `onstream` data extraction successfully. The only issue is that solana network is not known for archive capabilities, which means historical data might be incomplete or difficult to retrieve.

## Why now
We have some customer demand for more reliable and complete data extraction from the Solana network, which makes addressing the current limitations urgent.

## Next Steps
We need to explore solutions that can provide both real-time and historical data reliably, possibly by enhancing our current infrastructure or integrating with other data providers.


## Requirements
Create a deck explaining solutions for providing solana data to our customers (ie see the repo ../../cambrian/customer-lhava). Use `clickhouse-skill` for estimating data sizes and required work.

## View the deck

- [Interactive deck](./solana-data-paths.html)
- [PDF deck](./solana-data-paths.pdf)
- [Sources and assumptions](./sources-and-assumptions.html)

### Host locally with Python

With Python 3 installed, run this command from the repository root:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Open [http://127.0.0.1:8000/solana-data-paths.html](http://127.0.0.1:8000/solana-data-paths.html) in your browser. The [sources and assumptions](http://127.0.0.1:8000/sources-and-assumptions.html) page is served alongside the deck.

Keep the terminal running while viewing the deck. Press `Ctrl+C` to stop the server. If port 8000 is already in use, choose another port in the command and browser URL.

### Link to a slide

Add a slide anchor to the URL, for example [Common work](http://127.0.0.1:8000/solana-data-paths.html#common). Other examples are `#decision`, `#path-2`, `#elapsed-time`, and `#next-steps`. The URL updates as you navigate, so you can copy it to share the current slide. Browser Back and Forward restore previous slides.
