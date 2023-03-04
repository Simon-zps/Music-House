import React from "react";
import { Link, useParams } from 'react-router-dom';
import { useState, useEffect } from "react";
import { Grid, Button, Typography } from '@material-ui/core';
import CreateRoom from "./CreateRoom";
export default function Room(props) {

    let {code} = useParams();
    const [votesToSkip, setVotesToSkip] = useState(2);
    const [guestPausePermission, setGuestPausePermission] = useState(true);
    const [isHost, setIsHost] = useState(true);
    const [showSettings, setShowSettings] = useState(false); // relates to showing the actual settings page, not button
    
    //We need to fetch data regarding that code and display info, useEffect with empty array runs once

    useEffect(() => {
        fetch(`/api/room/${code}`,{
            method:'GET',
            headers:{
                'Content-Type':'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            setGuestPausePermission(data.guest_pause_permission);
            setIsHost(data.is_host);
            setVotesToSkip(data.votes_to_skip);
            console.log(data);
        });
    }, []);

    function handleChangeCode(newValue) {
        props.onChange(newValue);
        window.history.pushState({}, "","/");
    }

    function leaveRoom() {
        fetch(`/api/leave-room/${code}`,{
            method:"POST",
            headers: {
                'Content-Type':'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            handleChangeCode(data.code);
            window.location.href = "/";
        });
    }


    if(showSettings) {
        return (
            <Grid container spacing={0}>
                <Grid item xs={12} align="center">
                    <CreateRoom update={true} votesToSkip={votesToSkip} guestPausePermission={guestPausePermission} code={code}></CreateRoom>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button variant="contained" color="primary" onClick={()=>setShowSettings(false)}>Close</Button>
                </Grid>
            </Grid>
        );
    }
    

    return (
        <Grid container spacing={1}>
            <Grid item xs={12} align="center">
                <Typography variant="h4" component="h4">Room code: {code}</Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <Typography variant="h5" component="h5">Guest can pause: {guestPausePermission.toString()}</Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <Typography variant="h5" component="h5">Votes to skip: {votesToSkip}</Typography>
            </Grid>

            <Grid item xs={12} align="center">
                <Typography variant="h5" component="h5">Is Host: {isHost.toString()}</Typography>
            </Grid>

            { isHost && (
                <Grid item xs={12} align="center">
                <Button variant="contained" color="primary" onClick={()=>{setShowSettings(true)}}>Settings</Button>
                </Grid>
            ) }

            <Grid item xs={12} align="center">
                <Button variant="contained" color="secondary" onClick={leaveRoom} >Leave room</Button>
            </Grid>
        </Grid>
    );
}
/*<div id="room-info">
            <p>Room code: {code}</p>
            <p>Guest can pause: {guestPausePermission.toString()}</p>
            <p>Votes to skip: {votesToSkip}</p>
            <p>Is Host: {isHost.toString()}</p>
        </div>*/