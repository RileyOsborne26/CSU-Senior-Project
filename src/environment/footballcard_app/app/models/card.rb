class Card < ApplicationRecord
  # Define enums
  enum auto_ink_color: { black: 0, gold: 1, silver: 2, blue: 3, red: 4, green: 5, purple: 6 }
  enum grading_company: { psa: 0, bgs: 1, sgc: 2, hga: 3, csg: 4 }
  enum memorabilia_type: { jersey: 0, bat: 1, ball: 2, glove: 3, sock: 4, hat: 5, patch: 6, cleat: 7, shoe: 8, shoelace: 9, car: 10, tire: 11 }
  enum printing_plate: { black: 0, cyan: 1, magenta: 2, yellow: 3 }
end
