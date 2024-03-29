from aiogram.fsm.state import State, StatesGroup


class ClientAdsStates(StatesGroup):
    selectAdCategory = State()
    selectAdProduct = State()
    insertTitle = State()
    insertText = State()
    insertPrice = State()
    insertImages = State()
    insertPhone = State()

    showAllAds = State()
    showSearchResults = State()
    waiting_for_search_query = State()
    searchAds = State()