from aiogram.types import Message, ContentType, ShippingQuery, ShippingOption
from aiogram.types import PreCheckoutQuery, LabeledPrice
from aiogram.dispatcher.filters import Command

import json

from main import bot, dp

from keyboards import keyboard

from config import load_config
config = load_config('/workspaces/anton2010000.github.io/.env')
PAYMENTS_TOKEN = config.tg_bot.payments_token
@dp.message_handler(Command('start'))
async def start(message: Message):
    await bot.send_message(message.chat.id,
                           'Онлайн магазин в телеграм',
                           reply_markup=keyboard)

normal_shipping_options = ShippingOption(id='normal', title='Доставка за границу').add(LabeledPrice('Доставка за границу', 20000))


@dp.message_handler(content_types='web_app_data')
async def buy_process(web_app_message):
    orderItems = json.loads(web_app_message.web_app_data.data)
    description = ''
    sum = 0
    for item in orderItems:
        description += item.get('label') + " " + str(item.get('amount')/100) + "руб | "
        sum += item.get('amount')/100
    await bot.send_invoice(web_app_message.chat.id,
                           title='Заказ',
                           description='В заказе позиций: ' + str(len(orderItems)) + '. На сумму ' + str(sum) + ' руб',
                           provider_token=PAYMENTS_TOKEN,
                           photo_url='https://kawai.shikimori.one/assets/globals/missing_original.jpg',
                           photo_height=212,  # !=0/None or picture won't be shown
                           photo_width=212,
                           need_name=True,
                          # need_shipping_address=True,
                           send_email_to_provider=True,
                           is_flexible=True,
                           currency='rub',
                           need_email=True,
                           need_phone_number=True,
                           prices=json.loads(web_app_message.web_app_data.data),
                           start_parameter='example',
                           payload='some_invoice')
    await bot.send_message(web_app_message.chat.id, f"получили инофрмацию из веб-приложения: {web_app_message.web_app_data.data}")


@dp.shipping_query_handler(lambda q: True)
async def shipping_process(shipping_query: ShippingQuery):
    if shipping_query.shipping_address.country_code != "RU"\
            and shipping_query.shipping_address.country_code != "BY"\
            and shipping_query.shipping_address.country_code != "KZ":
        return await bot.answer_shipping_query(
            shipping_query.id,
            ok=False,
            error_message="По данному адресу нет доставки!"
        )
    shipping_options = [ShippingOption(id='regular',
                                    title='Доставка по России').add(LabeledPrice('Доставка по России', 00000))]

    if shipping_query.shipping_address.country_code =="KZ"\
            or shipping_query.shipping_address.country_code =="BY":
        shipping_options.append(normal_shipping_options)

    await bot.answer_shipping_query(
            shipping_query.id,
            ok=True,
            shipping_options=shipping_options
        )

@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message = "Sorry, someone bought the last item from the warehouse, "
                                                        "choose something else.")

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    await bot.send_message(message.chat.id,
                           'Платеж сумму `{} {}` совершен успешно!'.format(
                               message.successful_payment.total_amount / 100, message.successful_payment),
                           parse_mode='Markdown')
