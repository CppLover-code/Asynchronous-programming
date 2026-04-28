# Четыре основных механизма фактического запуска сопрограммы

"""
1. Основной цикл событий (точку входа верхнего уровня) можно 
запустить при помощи функция asyncio.run()
"""
import asyncio

async def main():
    print("hello")
    await asyncio.sleep(1)
    print("world")

asyncio.run(main())

"""
2. Запуск сопрограмм, которые должны или могут ждать каких-то результатов 
(например, ответа сервера с результатами запроса) запускаются оператором await.

Следующий фрагмент кода напечатает "hello" после ожидания в течение 1 секунды, 
а затем напечатает "world" после ожидания еще 2-х секунд:
"""
import asyncio, time

async def say_after(delay, what):
    # Асинхронная функция (сопрограмма)
    await asyncio.sleep(delay)
    print(what)

async def main():
    # Точка входа в асинхронную прошрамму
    print(f"started at {time.strftime("%X")}")

     # запуск сопрограммы `say_after()` происходит при  
    # помощи оператора `await`, т. к. в самой сопрограмме  
    # есть объект ожидания - неблокирующая функция 
    # `asyncio.sleep()`, которая эмитирует ожидание ответа сервера
    await say_after(1, 'hello')
    await say_after(2, "world")

    print(f"finished at {time.strftime('%X')}")
    
# запуск основного цикла событий
asyncio.run(main())

"""
3. Запуск сопрограмм можно осуществлять через создание и планирование задач при 
помощи функции asyncio.create_task(). Объекты задач Task также являются объектами 
ожидания результата, т.к. планируют запуск сопрограмм в будущем, как только это 
станет возможным. Следовательно задачи, то же запускаем оператором await
"""

import asyncio, time

async def say_after(delay, what):
    """Асинхронная функция (сопрограмма)"""
    await asyncio.sleep(delay)
    print(what)

async def main():
    """Точка входа в асинхронную программу"""

    # создаем задачи `task1` и `task2`
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Ждем, пока обе задачи будут выполнены 
    # (должно занять около 2 секунд.)
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())

# ВНИМАНИЕ! Фрагмент кода выполняется на 1 секунду быстрее, чем раньше!!!!

"""
4. ЗКласс asyncio.TaskGroup() (добавлен в Python 3.11) представляет собой более 
современную альтернативу asyncio.create_task(). Используя этот API, последний 
пример становится таким:
"""
import asyncio, time

async def say_after(delay, what):
    """Асинхронная функция (сопрограмма)"""
    await asyncio.sleep(delay)
    print(what)

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(say_after(1, "hello"))
        task2 = tg.create_task(say_after(2, "world"))

        print(f"started at {time.strftime("%X")}")
    
    # The wait is implicit when the context manager exits.
print(f"finished at {time.strftime('%X')}")

# Время и вывод должны быть такими же, как и для предыдущей версии.
