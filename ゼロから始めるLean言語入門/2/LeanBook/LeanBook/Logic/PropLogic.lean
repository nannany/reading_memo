#eval False → True

example (P Q : Prop) (h : P → Q) (hp : P) : Q := by
  apply h
  apply hp


example (P Q : Prop) (hq : Q) : P → Q := by
  intro hp
  apply hq
