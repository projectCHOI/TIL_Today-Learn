-- Skill slots are independent of physical/special damage categories.
return {
 axe_strike={name='도끼치기',category='physical',power=100,accuracy=80,cost=1,
  element='격투',metric='manhattan',minRange=1,maxRange=1,maxHeight=2},
 rampage={name='난동부리기',category='physical',power=50,accuracy=100,cost=2,
  element='격투',metric='chebyshev',minRange=1,maxRange=1,maxHeight=2,retaliation=true},
 test_strike={name='시험 공격',category='physical',power=40,accuracy=80,cost=1,
  element='노말',metric='manhattan',minRange=1,maxRange=1,maxHeight=2}
}
