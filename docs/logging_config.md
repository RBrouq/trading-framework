Le module `trading_framework.logging_config` permet de configurer facilement `loguru` :

```python
from trading_framework.logging_config import configure_logging

# Par défaut, rotation journalière et rétention 7 jours
configure_logging("logs/trading.log")