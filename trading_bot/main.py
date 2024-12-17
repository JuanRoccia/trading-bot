import os
from dotenv import load_dotenv
from loguru import logger
from trading_bot.data_collector import DataCollector
from trading_bot.signal_generator import SignalGenerator
from trading_bot.trade_executor import TradeExecutor
from apscheduler.schedulers.blocking import BlockingScheduler

# Cargar variables de entorno
load_dotenv()

class TradingBot:
    def __init__(self):
        # Configuración desde variables de entorno
        self.broker_token = os.getenv('BROKER_TOKEN')
        self.account_id = os.getenv('ACCOUNT_ID')
        self.instrument = os.getenv('TRADING_INSTRUMENT', 'EUR_USD')
        
        # Inicializar componentes
        self.data_collector = DataCollector(self.instrument)
        self.signal_generator = SignalGenerator()
        self.trade_executor = TradeExecutor(
            token=self.broker_token, 
            account_id=self.account_id
        )
        
        # Configurar logging
        logger.add("trading_bot.log", rotation="10 MB")

    def run_trading_cycle(self):
        try:
            # Recolectar datos
            latest_data = self.data_collector.get_latest_candles()
            
            # Generar señal de trading
            signal = self.signal_generator.generate_signal(latest_data)
            
            # Ejecutar trade si hay señal
            if signal:
                self.trade_executor.execute_trade(signal, latest_data)
                logger.info(f"Trade ejecutado: {signal}")
        
        except Exception as e:
            logger.error(f"Error en ciclo de trading: {e}")

    def start(self):
        # Configurar scheduler
        scheduler = BlockingScheduler()
        scheduler.add_job(
            self.run_trading_cycle, 
            'interval', 
            minutes=15,  # Ajustar según necesidad
            max_instances=1
        )
        
        logger.info("Iniciando Trading Bot...")
        scheduler.start()

def main():
    bot = TradingBot()
    bot.start()

if __name__ == "__main__":
    main()