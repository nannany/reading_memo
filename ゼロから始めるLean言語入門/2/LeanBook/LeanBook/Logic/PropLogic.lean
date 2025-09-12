#eval False → True

example (P Q : Prop) (h : P → Q) (hp : P) : Q := by
  apply h
  apply hp


example (P Q : Prop) (hq : Q) : P → Q := by
  intro hp
  apply hq


#eval ¬ True

example (P Q: Prop) (h1 : P → Q) (h2 : Q → P) : P ↔ Q := by
  constructor
  · apply h1
  · apply h2


example (P Q : Prop) (hq : Q) : (Q → P) ↔ P := by
  constructor

  case mp =>
    intro h
    exact h hq

  case mpr =>
    intro hp hq
    exact hp


  example (P Q : Prop): (¬ P ∨ Q) → (P → Q) := by
    intro h
    intro hp
    cases h with
    | inl hn =>
      exfalso
      apply hn
      exact hp
    | inr hq =>
      exact hq


  example (P Q : Prop) : ¬ (P ∨ Q) → (¬ P ∧ ¬ Q) := by
    intro h
    constructor

    case left =>
      intro hp
      apply h
      left
      exact hp

    case right =>
      intro hq
      apply h
      right
      exact hq
