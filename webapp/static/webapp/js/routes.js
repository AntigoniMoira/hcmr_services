export default {
    home:{
        root:'',
        map:'http://localhost:9000/api/platforms/?inst=7&status=true',
        latest_ts: 'http://localhost:9000/api/latest_ts/',
        latest_pr: 'http:/ /localhost:9000/api/latest_pr/',
        platforms_between: 'http://localhost:9000/webapp/platforms_between/',
        measurements_between: 'http://localhost:9000/webapp/measurements_between/',
        create_netcdf: 'http://localhost:9000/webapp/create_netcdf/',
        activate_user: 'http://localhost:9000/webapp/activate/',
        delete_user: 'http://localhost:9000/webapp/delete_user/',
        error: 'http://localhost:9000/webapp/error',
        user_profile: 'http://localhost:9000/webapp/user_profile/',
        change_password: 'http://localhost:9000/webapp/change_password/'
    },
    auth:{
        login: 'http://localhost:8000/o/authorize/',
        logout: 'http://localhost:9000/webapp/logout/',
    }

}
