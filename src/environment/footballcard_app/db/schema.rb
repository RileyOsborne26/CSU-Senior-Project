# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.0].define(version: 2024_06_23_024934) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "cards", primary_key: "card_id", force: :cascade do |t|
    t.string "year_id", limit: 7
    t.string "player_id", limit: 50
    t.string "team_id", limit: 50
    t.string "position_id", limit: 10
    t.string "set_id", limit: 50
    t.string "card_number", limit: 10
    t.boolean "is_serial_numbered"
    t.integer "print_run"
    t.integer "serial_number"
    t.string "parallel_color", limit: 25
    t.string "parallel_type", limit: 15
    t.boolean "is_autographed"
    t.boolean "is_dual_auto"
    t.integer "auto_ink_color"
    t.boolean "is_graded"
    t.integer "grading_company"
    t.string "grade_id", limit: 15
    t.decimal "grade_number", precision: 1, scale: 3
    t.decimal "corners_subgrade_number", precision: 1, scale: 3
    t.decimal "surface_subgrade_number", precision: 1, scale: 3
    t.decimal "edges_subgrade_number", precision: 1, scale: 3
    t.decimal "centering_subgrade_number", precision: 1, scale: 3
    t.string "subset_id", limit: 20
    t.boolean "is_case_hit"
    t.boolean "is_memorabilia"
    t.integer "memorabilia_type"
    t.integer "memorabilia_pieces_number", limit: 2
    t.boolean "is_booklet"
    t.integer "printing_plate"
    t.boolean "is_mini"
    t.string "sport_id", limit: 15
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["grade_id"], name: "index_cards_on_grade_id", unique: true
    t.index ["player_id"], name: "index_cards_on_player_id"
    t.index ["set_id"], name: "index_cards_on_set_id"
    t.index ["team_id"], name: "index_cards_on_team_id"
    t.index ["year_id"], name: "index_cards_on_year_id"
  end

  create_table "owned_cards", primary_key: "user_card_id", force: :cascade do |t|
    t.bigint "user_id", null: false
    t.bigint "card_id", null: false
    t.boolean "ownership_status"
    t.datetime "date_created"
    t.decimal "entry_market_value", precision: 10, scale: 2
    t.boolean "is_anonymous"
    t.boolean "is_for_trade"
    t.boolean "is_for_sale"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["card_id"], name: "index_owned_cards_on_card_id"
    t.index ["user_id"], name: "index_owned_cards_on_user_id"
  end

  create_table "price_histories", primary_key: "card_price_id", force: :cascade do |t|
    t.bigint "user_card_id_id", null: false
    t.datetime "price_date"
    t.decimal "market_value", precision: 10, scale: 2
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["user_card_id_id"], name: "index_price_histories_on_user_card_id_id"
  end

  create_table "transaction_histories", primary_key: "transaction_id", force: :cascade do |t|
    t.bigint "buyer_user_id_id", null: false
    t.bigint "user_card_id_id", null: false
    t.integer "type"
    t.datetime "transaction_date"
    t.decimal "price", precision: 10, scale: 2
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["buyer_user_id_id"], name: "index_transaction_histories_on_buyer_user_id_id"
    t.index ["user_card_id_id"], name: "index_transaction_histories_on_user_card_id_id"
  end

  create_table "users", primary_key: "user_id", force: :cascade do |t|
    t.string "first_name"
    t.string "email"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "password_digest"
    t.boolean "admin", default: false
    t.string "username", limit: 25
    t.string "last_name", limit: 25
    t.index ["email"], name: "index_users_on_email", unique: true
    t.index ["user_id"], name: "index_users_on_user_id", unique: true
    t.index ["username"], name: "index_users_on_username", unique: true
  end

  create_table "wish_lists", primary_key: "wish_id", force: :cascade do |t|
    t.bigint "user_id_id", null: false
    t.bigint "card_id_id", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["card_id_id"], name: "index_wish_lists_on_card_id_id"
    t.index ["user_id_id"], name: "index_wish_lists_on_user_id_id"
  end

  add_foreign_key "owned_cards", "cards", primary_key: "card_id"
  add_foreign_key "owned_cards", "users", primary_key: "user_id"
  add_foreign_key "price_histories", "owned_cards", column: "user_card_id_id", primary_key: "user_card_id"
  add_foreign_key "transaction_histories", "owned_cards", column: "user_card_id_id", primary_key: "user_card_id"
  add_foreign_key "transaction_histories", "users", column: "buyer_user_id_id", primary_key: "user_id"
  add_foreign_key "wish_lists", "cards", column: "card_id_id", primary_key: "card_id"
  add_foreign_key "wish_lists", "users", column: "user_id_id", primary_key: "user_id"
end
