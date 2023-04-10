const express=require('express')
const mysql=require('mysql')
const cors=require('cors')


const app=express()
app.use(cors())
app.use(express.json())

const db=mysql.createConnection({
    host:"localhost",
    user:"root",
    password:"",
    database:"account",
})

app.post('/create',(req,res)=>{
    const query="insert into login (`Username`,`Email`,`Pass`) values (?)"
    const values=[
        req.body.Username,
        req.body.Email,
        req.body.Pass,
    ]
    db.query(query,[values],(err,data)=>{
        if(err){
            return res.json("Error")
        }
        return res.json(data)
    })
})

app.post('/login',(req,res)=>{
    const query="select * from login where `Username` = ? and `Pass` = ?"
    db.query(query,[req.body.Username,req.body.Pass],(err,data)=>{
        if(err){
            return res.json("Error")
        }
        if(data.length>0){
            return res.json("Success")
        }
        else{
            return res.json("Fail")
        }
    })
})

app.post('/tracking',(req,res)=>{
    const query="with Q1(ID) as (select ID_patient from list_tracking where `User`= ?)\
            select information.ID_patient,Name,Age,Address from Q1 inner join information\
            on Q1.ID=information.ID_patient"
    db.query(query,[req.body.Username],(err,data)=>{
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
    const query="select * from information where `ID_patient`=?"
    db.query(query,[req.body.ID],(err,data)=>{
        if(err){
            return res.json("Error")
        }
        return res.json(data)
    })
})

app.post('/addtracking',(req,res)=>{
    const query="insert into list_tracking (`User`,`ID_patient`) values(?)"
    const values=[
        req.body.Username,
        req.body.ID_patient,
    ]
    db.query(query,[values],(err,data)=>{
        if(err){
            return res.json(err)
        }
        return res.json(data)
    })
})


app.listen(3000,()=>{
    console.log("Listening at port 3000")
})

