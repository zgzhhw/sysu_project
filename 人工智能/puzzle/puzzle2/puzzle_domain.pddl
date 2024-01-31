(define (domain puzzle)
  (:requirements :strips :equality:typing)
  (:types num loc) 
  (:predicates  
    (at ?n - num ?l - loc)
    (adjacent ?x ?y - loc)
    (empty ?x - loc))

(:action slide
      :parameters (?t - num  ?x ?y - loc)
      :precondition (and (at ?t ?x) (empty ?y) (adjacent ?x ?y))
      :effect (and (at ?t ?y) (not (empty ?y)) (empty ?x) (not(at ?t ?x)) ) 
 )
)