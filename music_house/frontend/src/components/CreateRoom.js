import React from "react";
import { Button, Grid, Typography, TextField, FormHelperText, FormControl, FormControlLabel, RadioGroup, Radio } from "@mui/material";
import { Link } from 'react-router-dom';
import { Collapse } from "@material-ui/core";
import { useState } from "react";


export default function CreateRoom(props) {

    const [votesToSkip, setVotesToSkip] = useState(props.votesToSkip);
    function handleVotesChange(e) {
        setVotesToSkip(e.target.value);
    }

    const [guestPausePermission, setGuestPausePermission] = useState(true);
    function handleGuestPausePermission(e) {
        setGuestPausePermission(e.target.value === 'true');
    }

    

    function handleCreateRoomButtonPressed(){
        let url = '/api/create-room'
        fetch(url, {
            method:'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                votes_to_skip:votesToSkip,
                guest_pause_permission:guestPausePermission,
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Data:", data)
            const redirectUrl = `/room/${data.code}`;
            window.location.href = redirectUrl;
        })
        .catch(error => {
            console.error("Error creating", error);
        });
    }

    function handleUpdateRoomButtonPressed(){
        let url = '/api/update-room'
        fetch(url, {
            method:'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                votes_to_skip: votesToSkip,
                guest_pause_permission: guestPausePermission,
                code: props.code,
            })
        })
        .then(response => {
            if(response.ok){
                props.setMessage("Successfuly updated room");
            }
            return response.json()})
        .then(data => {
            console.log("Data:", data)
        })
        .catch(error => {
            console.error("Error updating", error);
        });
    }


    function createButtonsRenderer() {
        return (
            <>
            <Grid item xs={12} align="center">
                <Button color="secondary" variant="contained" onClick={handleCreateRoomButtonPressed} >Create a room</Button>
            </Grid>

            <Grid item xs={12} align="center">
                <Button color="primary" variant="contained" component={Link} to="/">Go back</Button>
            </Grid>
            </>
        );
    }

    function updateButtonsRenderer() {
        return (
            <>
            <Grid item xs={12} align="center">
                <Button color="secondary" variant="contained" onClick={handleUpdateRoomButtonPressed} >Update room</Button>
            </Grid>
            </>
        );
    }

    return (
        <Grid container spacing={0} className="grid-container" >

            <Grid item xs={12} align="center">
                <Collapse in={props.message != ""} >
                    {props.message}
                </Collapse>
            </Grid>

            <Grid item xs={12} align="center">
                <Typography component='h4' variant='h4' >
                    { props.update ? "Update" : "Create" } room {props.code}
                </Typography>
            </Grid>
            
            <Grid item xs={12} align="center">
                <FormControl component="fieldset" >
                    <FormHelperText>
                        <div align="center">Guests pause permission</div>
                    </FormHelperText>

                    <RadioGroup row defaultValue="true" onChange={handleGuestPausePermission}>
                        <FormControlLabel value="true" control={<Radio color="primary" />} label="Play/Pause" labelPlacement="bottom" />
                        <FormControlLabel value="false" control={<Radio color="secondary" />} label="No control" labelPlacement="bottom" />
                    </RadioGroup>
                </FormControl>
            </Grid>

            <Grid item xs={12} align="center">
                <FormControl>
                    <TextField required={true} type="number" onChange={handleVotesChange} defaultValue={props.votesToSkip} inputProps={{min:1, style:{textAlign:"center"}}}/>
                    <FormHelperText>
                        <div align="center">
                            Votes required to skip song
                        </div>
                    </FormHelperText>
                </FormControl>
            </Grid>

            { props.update ?  updateButtonsRenderer() : createButtonsRenderer()}
            
        </Grid>
    );
}

