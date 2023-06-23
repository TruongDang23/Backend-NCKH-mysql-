const express=require('express')
const mysql=require('mysql')
const cors=require('cors')
const moment=require('moment')
const app=express()

app.use(cors())
app.use(express.json())


const db=mysql.createConnection({
    host:"103.130.211.150",
    port:"10039",
    user:"nckh",
    password:"nckhfit",
    database:"mydb",
})

app.post('/create',(req,res)=>{
    const query="insert into logins (`Username`,`Email`,`Pass`,`ID`) values (?)"
    const values=[
        req.body.Username,
        req.body.Email,
        req.body.Pass,
        req.body.ID,
    ]
    db.query(query,[values],(err,data)=>{
        if(err){
            return res.json("Error")
        }
        return res.json(data)
    })
})

app.post('/login',(req,res)=>{
    const query="select * from logins where `Username` = ? and `Pass` = ?"
    db.query(query,[req.body.Username,req.body.Pass],(err,data)=>{
        if(err){
            return res.json("Error")
        }
        if(data.length>0){
            return res.json(data)
        }
        else{
            return res.json("Fail")
        }
    })
})

app.post('/tracking',(req,res)=>{
    const query="with Q1(ID) as (select ID_patient from mydb.list_tracking where `User`= ?) select information.ID_patient,Name,Age,Address from mydb.information inner join Q1 on Q1.ID=information.ID_patient"
            
    db.query(query,[req.body.ID],(err,data)=>{
        if(err){
            return res.json("Error")
        }
        return res.json(data)
    })
})

app.post('/mornitor',(req,res)=>{
    const realDate= moment().format("YYYY-MM-DD")
    const query="select Time,HeartRate,Oxi,GripStrength from mornitor where `ID_patient`=? and DATE(`Time`)='"+realDate+"'"
    db.query(query,[req.body.ID],(err,data)=>{
        if(err){
            return res.json("Error")
        }
        return res.json(data)
    })
})

app.post('/estimate',(req,res)=>{
    const query="select * from estimate where `ID_patient` = ?"
    db.query(query,[req.body.ID],(err,data)=>{
        if(err){
            return res.json("Error")
        }
        return res.json((data))
    })
})

app.post('/find',(req,res)=>{
    const query="select * from information where `Name`=?"
    db.query(query,[req.body.Name],(err,data)=>{
        if(err){
            return res.json("Error")
        }
        return res.json(data)
    })
})

app.post('/addtracking',(req,res)=>{
    const query="insert into list_tracking (`User`,`ID_patient`) values(?)"
    const values=[
        req.body.ID,
        req.body.ID_patient,
    ]
    db.query(query,[values],(err,data)=>{
        if(err){
            return res.json(err)
        }
        return res.json(data)
    })
})

app.post('/deletetracking',(req,res)=>{
    const query="delete from list_tracking where `User` = ? and `ID_patient` = ?"
    db.query(query,[req.body.ID,req.body.ID_patient],(err,data)=>{
        if(err){
            return res.json(err)
        }
        return res.json(data)
    })
})

app.post('/count',(req,res)=>{
    const query="select count(*) as Count from mydb.logins"
    db.query(query,(err,data)=>{
        if(err){
            return res.json(err)
        }
        return res.json(data)
    })
})

app.listen(3000) //Open port 3000
