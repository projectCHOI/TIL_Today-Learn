return {name='Mortarion',portrait='Mortarion.png',korean='모리타운',job='소환사',equipment='책(book)',element='악',deployable=true,
 stats={25,20,15,105,55,90},ranks={{25,20,15,105,55,90},{40,35,30,120,70,105},{55,50,45,135,95,120}},
 promotions={{skill='summon_elemental',count=3},{skill='summon_greater_elemental',count=3}},
 combatSkills={'summon_elemental','elemental_bomb','hypnosis','summon_greater_elemental','elemental_wrath','necromancer'},
 skills={'정령소환','정령 폭탄','최면술','중급 정령소환','정령의 분노','귀환'},
 summons={image='assets/images/mob_Fruit_d.png',capacityByGrade={lower=5,middle=5},
  explosion={offsets={
   lower={{-1,-1},{0,-1},{1,-1},{-1,0},{1,0},{-1,1},{0,1},{1,1}},
   middle={{-1,-2},{0,-2},{1,-2},{-1,-1},{0,-1},{1,-1},{-2,0},{-1,0},{1,0},{2,0},
    {-1,1},{0,1},{1,1},{-1,2},{0,2},{1,2}}
  }}},provisionalRules='src.rules'}
