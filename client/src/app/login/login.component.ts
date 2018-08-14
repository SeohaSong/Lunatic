import { Component, OnInit } from '@angular/core';

import { HttpClient } from '@angular/common/http';
import { Router } from "@angular/router";


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(
    private http: HttpClient,
    private router: Router
  ) { }

  user_id: string;
  user_pw: string;

  ngOnInit() {
    if(window.localStorage.getItem('token')) {
      this.router.navigate(['main']);
    }
  }

  request_login() {
    let user = {uid: this.user_id, password: this.user_pw}
    this.http.post(
      'http://10.16.129.116:3000/api/auth/login', user
    ).subscribe((data) => {
      console.log(data)
      if(data['success']) {
        window.localStorage.setItem('token', data['data']);
        this.router.navigate(['main']);
      }
    });
  }

}
