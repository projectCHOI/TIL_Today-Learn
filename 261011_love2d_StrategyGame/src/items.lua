local Items={
 {name='체리', heal=10, image='mob_Fruit_a.png'},
 {name='바나나', heal=20, image='mob_Fruit_b.png'},
 {name='오렌지', heal=30, image='mob_Fruit_c.png'},
 {name='사과', heal=40, image='mob_Fruit_d.png'},
 {name='빨간 포션', heal=100, image='mob_item_Life.png'}
}

local elements={'노말','격투','독','벌레','불꽃','물','전기','얼음','고스트','페어리','악','드래곤'}
for index,element in ipairs(elements) do
 Items[#Items+1]={
  name=element..' 보석',
  element=element,
  image=string.format('mob_Jewelry_%02d.png',index)
 }
end
return Items
