ERROR_TRANSACTION_LIST={
  "code": 404,
  "message": {
    "error": "current account have no transaction history"
  },
  "status": "Not Found"
}

ERROR_CREATE_TRANSACTION={
  "code": 406,
  "message": {
    "available_transaction_type": [
      "budgets",
      "deposit",
      "entertainment",
      "groceries",
      "receive",
      "rent",
      "transfer",
      "withdrawal"
    ],
    "error_text": "acount with id : 7a28ed48-ab6d-4f1a-87ca-f918301047bf have not enough money, "
  },
  "status": "Not Acceptable"
}
ERROR_TRANSACTION_NOT_FOUND={
  "code": 404,
  "message": "transaction not found",
  "status": "Not Found"
}
ERROR_TRANSACTION_CATEGORY_NOT_FOUND={
  "code": 404,
  "message": "user does't have any transaction  records",
  "status": "Not Found"
}