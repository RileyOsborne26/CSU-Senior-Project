class OwnerHistory < ApplicationRecord
  belongs_to :user_id
  belongs_to :card_id
end
