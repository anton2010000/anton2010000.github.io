from aiogram.types import Message, ContentType, ShippingQuery, ShippingOption
from aiogram.types import PreCheckoutQuery, LabeledPrice
from aiogram.dispatcher.filters import Command

from main import bot, dp
from config import PAYMENTS_TOKEN

from keyboards import keyboard

@dp.message_handler(Command('start'))
async def start(message: Message):
    await bot.send_message(message.chat.id,
                           'Тестируем WebAppss',
                           reply_markup=keyboard)

PRICE = {
    '1': [LabeledPrice(label='Item1', amount=10000)],
    '2': [LabeledPrice(label='Item2', amount=200000)],
    '3': [LabeledPrice(label='Item3', amount=30000)],
    '4': [LabeledPrice(label='Item4', amount=400000)],
    '5': [LabeledPrice(label='Item5', amount=500000)],
    '6': [LabeledPrice(label='Item6', amount=600000)]
}

normal_shipping_options = ShippingOption(id='normal', title='Быстрая доставка').add(LabeledPrice('Быстрая доставка ', 20000))

@dp.message_handler(content_types='web_app_data')
async def buy_process(web_app_message):
    await bot.send_invoice(web_app_message.chat.id,
                           title='Product name,',
                           description='Product description',
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
                           prices=PRICE[f'{web_app_message.web_app_data.data}'],
                           start_parameter='example',
                           payload='some_invoice')

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
                                    title='Бесплатная доставка').add(LabeledPrice('Бесплатная доставка', 00000))]

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

                           'Платеж совершен успешно!')