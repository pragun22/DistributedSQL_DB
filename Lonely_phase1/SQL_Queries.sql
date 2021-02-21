-- query to find all the fragments and its site info 
SELECT id, SiteId FROM Fragments where RelationName='[Table_name]'

-- query to find the site given an fragment id
select S.id, `IP/BindAddress` from Site S join Fragments F on S.id = F.SiteId where F.id = [FragmentId];


-- An alternative way to perform that query
Select `IP/BindAddress` from Site where id in (Select SiteId from Fragments where id = [FragmentId]);
