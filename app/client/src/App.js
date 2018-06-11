import React, { Component } from 'react';
import { Row, Col, Switch, Slider, Card, Select } from 'antd';
import axios from 'axios';
import './App.css';
import rink from './full-rink.png';
import player from './player.svg';
import base64 from 'base-64';

import $ from 'jquery';

const Option = Select.Option;

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      'shotType': 'WRIST',
      'shotOnEmptyNet': false,
      'shotRebound': false,
      'shotRush': false,
      'shotDistance': 10,
      'shotAngle': 0,
      'shotAngleAdjusted': 0,
      'prediction': 0,
      'playerX': 92,
      'playerY': 220,
      'requestJSON': {},
      'responseJSON': {}
    };
  }

  componentWillMount() {
    this.getProb();
    this.calcPlayerPosition();
  }

  onReboundChange = () => {
    const prevState = this.state.shotRebound;
    this.setState({
      'shotRebound': !prevState
    }, () => this.getProb());
  }

  onRushChange = () => {
    const prevState = this.state.shotRush;
    this.setState({
      'shotRush': !prevState
    }, () => this.getProb());
  }

  onEmptyNetChange = () => {
    const prevState = this.state.shotOnEmptyNet;
    this.setState({
      'shotOnEmptyNet': !prevState
    }, () => this.getProb());
  }

  handleShotChange = (value) => {
    this.setState({
      'shotType': value
    }, () => this.getProb());
  }

  handleDistanceChange = (value) => {
    this.setState({
      'shotDistance': value
    }, () => {
      this.getProb();
      this.calcPlayerPosition();
    });
  }

  handleAngleChange = (value) => {
    const shotAngleAdjusted = Math.abs(value);
    this.setState({
      'shotAngle': value,
      shotAngleAdjusted
    }, () => {
      this.getProb();
      this.calcPlayerPosition();
    });
  }

  calcPlayerPosition = () => {
    const { shotDistance, shotAngle } = this.state;
    const offsetX = 92;
    const offsetY = 220;
    const PPF = 1200 / 200;

    const shotAngleRad = -1 * shotAngle * Math.PI / 180;
    const xLoc = Math.cos(shotAngleRad) * shotDistance;
    const yLoc = Math.sin(shotAngleRad) * shotDistance;

    const xLocAdj = (xLoc * PPF) + offsetX;
    const yLocAdj = (yLoc * PPF) + offsetY;

    console.log(xLocAdj)
    console.log(yLocAdj)

    this.setState({
      playerX: xLocAdj,
      playerY: yLocAdj
    })
  }

  getProb = () => {
    const { shotType, shotOnEmptyNet, shotRebound, shotRush, shotDistance, shotAngleAdjusted } = this.state;
    const postData = {
      shotType,
      shotOnEmptyNet,
      shotRebound,
      shotRush,
      shotDistance,
      shotAngleAdjusted
    }
    console.log(postData)
    axios.post('/predict', postData)
      .then(resp => {
        console.log(resp);
        if (resp.data.prediction) {
          this.setState({ prediction: resp.data.prediction });
        }
      })
  }

  render() {
    const { prediction, playerX, playerY } = this.state;
    const predictionPercent = (prediction * 100).toFixed(1)
    console.log(playerX);
    console.log(playerY);
    const playerStyles = {width: "45px", position: "absolute", top: `${this.state.playerY}px`, left: `${playerX}px`};
    console.log(playerStyles);

    return (
      <div className="App">
        <Row gutter={16} type="flex" justify="space-around" align="middle">
          <Col className="gutter-row" span={6} align="middle">
            <Card style={{ width: 300 }}>
              <h2>Goal Probability: <b>{predictionPercent}%</b></h2>
            </Card>
            <br />
            <Card style={{ width: 300 }}>
              Shot Distance: <b>{this.state.shotDistance} ft</b>
              <Slider defaultValue={10} min={0} max={50} onAfterChange={this.handleDistanceChange}/>
              Shot Angle: <b>{this.state.shotAngle} deg</b>
              <Slider defaultValue={0} min={-90} max={90} step={5} onAfterChange={this.handleAngleChange}/>
              <br />
              Rebound Shot? <Switch onChange={this.onReboundChange} checkedChildren="True" unCheckedChildren="False" />
              <br /><br />
              Rush Shot? <Switch onChange={this.onRushChange} checkedChildren="True" unCheckedChildren="False" />
              <br /><br />
              Empty Net Shot? <Switch onChange={this.onEmptyNetChange} checkedChildren="True" unCheckedChildren="False" />
              <br /><br />
              Shot Type:
              <Select defaultValue="WRIST" style={{ marginLeft: "5px", width: 120 }} onChange={this.handleShotChange}>
                <Option value="WRIST">Wrist</Option>
                <Option value="BACK">Back</Option>
                <Option value="SLAP">Slap</Option>
                <Option value="TIP">Tip</Option>
                <Option value="WRAP">Wrap</Option>
                <Option value="DEFL">Deflection</Option>
              </Select>
            </Card>
          </Col>
          <Col className="gutter-row" span={18}>
            <img src={player} style={playerStyles} />
            <img src={rink} className="rink-image"/>
          </Col>
        </Row>
      </div>
    );
  }
}

export default App;
