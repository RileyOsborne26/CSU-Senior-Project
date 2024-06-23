class TransactionHistory < ApplicationRecord
  belongs_to :buyer_user_id
  belongs_to :user_card_id
end
