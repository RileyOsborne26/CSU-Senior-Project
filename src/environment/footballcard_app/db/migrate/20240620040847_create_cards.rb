class CreateCards < ActiveRecord::Migration[7.0]
  def change
    create_table :cards do |t|
      t.primary_key :card_id
      t.string :year_id, limit: 7
      t.string :player_id, limit: 50
      t.string :team_id, limit: 50
      t.string :position_id, limit: 10
      t.string :set_id, limit: 50
      t.string :card_number, limit: 10
      t.boolean :is_serial_numbered
      t.integer :print_run, limit: 4
      t.integer :serial_number, limit: 4
      t.string :parallel_color, limit: 25
      t.string :parallel_type, limit: 15
      t.boolean :is_autographed
      t.boolean :is_dual_auto
      t.integer :auto_ink_color
      t.boolean :is_graded
      t.integer :grading_company
      t.string :grade_id, limit: 15
      t.integer :grade_number, limit: 2
      t.integer :corners_subgrade_number, limit: 2
      t.integer :surface_subgrade_number, limit: 2
      t.integer :edges_subgrade_number, limit: 2
      t.integer :centering_subgrade_number, limit: 2
      t.string :subset_id, limit: 20
      t.boolean :is_case_hit
      t.boolean :is_memorabilia
      t.integer :memorabilia_type
      t.integer :memorabilia_pieces_number, limit: 2
      t.boolean :is_booklet
      t.integer :printing_plate
      t.boolean :is_mini
      t.string :sport_id, limit: 15

      t.timestamps
    end
    add_index :cards, :year_id
    add_index :cards, :player_id
    add_index :cards, :team_id
    add_index :cards, :set_id
    add_index :cards, :grade_id, unique: true
  end
end
