import time
from pip._internal.cli.main import main

# todo убрать когда-то
while True:
    try:
        import lxml

        break
    except ModuleNotFoundError:
        main(["install", "-U", "lxml>=5.3.0"])
while True:
    try:
        import bcrypt

        break
    except ModuleNotFoundError:
        main(["install", "-U", "bcrypt>=4.2.0"])
import Utils.cardinal_tools
import Utils.config_loader as cfg_loader
from first_setup import first_setup
from colorama import Fore, Style
from Utils.logger import LOGGER_CONFIG
import logging.config
import colorama
import sys
import os
from cardinal import Cardinal
import Utils.exceptions as excs
from locales.localizer import Localizer

logo = "FUNPAY Functional"

VERSION = "0.1.15.8"

Utils.cardinal_tools.set_console_title(f"FunPay Cardinal v{VERSION}")

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(__file__))

folders = ["configs", "logs", "storage", "storage/cache", "storage/plugins", "storage/products", "plugins"]
for i in folders:
    if not os.path.exists(i):
        os.makedirs(i)

files = ["configs/auto_delivery.cfg", "configs/auto_response.cfg"]
for i in files:
    if not os.path.exists(i):
        with open(i, "w", encoding="utf-8") as f:
            ...

colorama.init()

logging.config.dictConfig(LOGGER_CONFIG)
logging.raiseExceptions = False
logger = logging.getLogger("main")
logger.debug("------------------------------------------------------------------")

print(f"{Style.RESET_ALL}{logo}")
print(f"{Fore.RED}{Style.BRIGHT}v{VERSION}{Style.RESET_ALL}\n")  # locale
print(f"{Fore.MAGENTA}{Style.BRIGHT}By {Fore.BLUE}{Style.BRIGHT}Woopertail, @sidor0912, @thepazitivik{Style.RESET_ALL}")
print(
    f"{Fore.MAGENTA}{Style.BRIGHT} * GitHub: {Fore.BLUE}{Style.BRIGHT}github.com/thepazivikk/fpf{Style.RESET_ALL}")
print(f"{Fore.MAGENTA}{Style.BRIGHT} * Telegram: {Fore.BLUE}{Style.BRIGHT}t.me/thepazitivik")
print(f"{Fore.MAGENTA}{Style.BRIGHT} * Новости о обновлениях: {Fore.BLUE}{Style.BRIGHT}t.me/fpc_updates")
print(f"{Fore.MAGENTA}{Style.BRIGHT} * Плагины: {Fore.BLUE}{Style.BRIGHT}t.me/fpc_plugins")
print(f"{Fore.MAGENTA}{Style.BRIGHT} * Bio: {Fore.BLUE}{Style.BRIGHT}t.me/biopazik")
print(f"{Fore.MAGENTA}{Style.BRIGHT} * Telegram-чат: {Fore.BLUE}{Style.BRIGHT}t.me/funpay_cardinal")

if not os.path.exists("configs/_main.cfg"):
    first_setup()
    sys.exit()

if sys.platform == "linux" and os.getenv('FPC_IS_RUNNIG_AS_SERVICE', '0') == '1':
    import getpass

    pid = str(os.getpid())
    pidFile = open(f"/run/FunPayCardinal/{getpass.getuser()}/FunPayCardinal.pid", "w")
    pidFile.write(pid)
    pidFile.close()

    logger.info(f"$GREENPID файл создан, PID процесса: {pid}")  # locale

directory = 'plugins'
for filename in os.listdir(directory):
    if filename.endswith(".py"):  # Проверяем, что файл имеет расширение .py
        filepath = os.path.join(directory, filename)  # Получаем полный путь к файлу
        with open(filepath, 'r', encoding='utf-8') as file:
            data = file.read()  # Читаем содержимое файла
        # Заменяем подстроку
        if '"<i>Разработчик:</i> " + CREDITS' in data or " lot.stars " in data or " lot.seller " in data:
            data = data.replace('"<i>Разработчик:</i> " + CREDITS', '"sidor0912"') \
                .replace(" lot.stars ", " lot.seller.stars ") \
                .replace(" lot.seller ", " lot.seller.username ")
            # Сохраняем изменения обратно в файл
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(data)

try:
    logger.info("$MAGENTAЗагружаю конфиг _main.cfg...")  # locale
    MAIN_CFG = cfg_loader.load_main_config("configs/_main.cfg")
    localizer = Localizer(MAIN_CFG["Other"]["language"])
    _ = localizer.translate

    logger.info("$MAGENTAЗагружаю конфиг auto_response.cfg...")  # locale
    AR_CFG = cfg_loader.load_auto_response_config("configs/auto_response.cfg")
    RAW_AR_CFG = cfg_loader.load_raw_auto_response_config("configs/auto_response.cfg")

    logger.info("$MAGENTAЗагружаю конфиг auto_delivery.cfg...")  # locale
    AD_CFG = cfg_loader.load_auto_delivery_config("configs/auto_delivery.cfg")
except excs.ConfigParseError as e:
    logger.error(e)
    logger.error("Завершаю программу...")  # locale
    time.sleep(5)
    sys.exit()
except UnicodeDecodeError:
    logger.error("Произошла ошибка при расшифровке UTF-8. Убедитесь, что кодировка файла = UTF-8, "
                 "а формат конца строк = LF.")  # locale
    logger.error("Завершаю программу...")  # locale
    time.sleep(5)
    sys.exit()
except:
    logger.critical("Произошла непредвиденная ошибка.")  # locale
    logger.warning("TRACEBACK", exc_info=True)
    logger.error("Завершаю программу...")  # locale
    time.sleep(5)
    sys.exit()

localizer = Localizer(MAIN_CFG["Other"]["language"])

try:
    Cardinal(MAIN_CFG, AD_CFG, AR_CFG, RAW_AR_CFG, VERSION).init().run()
except KeyboardInterrupt:
    logger.info("Завершаю программу...")  # locale
    sys.exit()
except:
    logger.critical("При работе Кардинала произошла необработанная ошибка.")  # locale
    logger.warning("TRACEBACK", exc_info=True)
    logger.critical("Завершаю программу...")  # locale
    time.sleep(5)
    sys.exit()
