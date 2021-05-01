import React, {
useRef, 
useEffect, 
useState, 
useImperativeHandle, 
forwardRef
} from 'react'

import BaseCalendar from 'tui-calendar'
import dayjs from 'dayjs'

const CustomTuiCalendar = forwardRef(
  (
    {
      defaultView = "week",
      calendars = [], 
      schedules = [],
      onBeforeCreateSchedule = ()=>false,
      onBeforeUpdateSchedule = ()=>false, 
      onBeforeDeleteSchedule = ()=>false,
      ...rest
    }, 
    ref

  ) =>  {
    const calendarInstRef = useRef(null)
    const tuiRef = useRef(null)
    const [renderRange, setRenderRange] = useState("")
    const [startDayOfWeek, setStartDayOfWeek] = useState(1)
    const [type, setType] = useState("weekly")
    const [checkedCalendars, setCheckedCalendars] = useState(
      calendars.map((element)=> ({...element, isChecked:true}))
    )
    const [filterSchedules, setFilterSchedules] = useState(schedules)

    //useImperativeHandle

    useEffect(() => {
      calendarInstRef.current = new BaseCalendar(tuiRef.current, {
        useDetailPopup:false,
        useCreationPopup:false,
        scheduleView: ['time'],
        template:{
          timegridDisplayPrimayTime: function (time) {
            return (time.hour < 10 ? '0' : '') + time.hour + ':' + time.minutes + '0';
          },
          timegridDisplayTime: function (time) {
            return (time.hour < 10 ? '0' : '') + time.hour + ':' + time.minutes + '0';
          },

          time: function(schedule) {
            return schedule.title + ' <i class="fa fa-refresh"></i>' + schedule.raw;
          },
          
        },
        calendars, 
        schedules, 
        ...rest
      })
      setRenderRangeText()
      // render schedules
      calendarInstRef.current.clear()
      calendarInstRef.current.createSchedules(filterSchedules, true)
      calendarInstRef.current.render()

      calendarInstRef.current.on("beforeCreateSchedule", function(event){
        onBeforeCreateSchedule(event)
      })

      calendarInstRef.current.on("beforeUpdateSchedule", function(event){
        onBeforeUpdateSchedule(event)
      })

      calendarInstRef.current.on("beforeDeleteSchedule", function(event){
        onBeforeDeleteSchedule(event)
      })

      calendarInstRef.current.on("clickSchedule", function(event){
        //
      })

      calendarInstRef.current.on("clickDayname", function(event){
        if(calendarInstRef.current.getViewName()==="week"){
          calendarInstRef.current.setDate(new Date(event.date))
          calendarInstRef.current.changeView("day", true)
        }
      })

      calendarInstRef.current.on("clickMore", function (event) {
        // console.log("clickMore", event.date, event.target);
      });

      calendarInstRef.current.on("clickTimezonesCollapseBtn", function (
        timezonesCollapsed
      ) {
        // console.log(timezonesCollapsed);
      });

      calendarInstRef.current.on("afterRenderSchedule", function (event) {
        // var schedule = event.schedule;
        // var element = calendarInstRef.current.getElement(
        //   schedule.id,
        //   schedule.calendarId
        // );
        // use the element
        // console.log(element);
      });

      return () => {
        calendarInstRef.current.destroy()
      }
     
    }, [schedules, tuiRef]);

    const currentCalendarDate = (format) => {
      var currentDate = dayjs([
        calendarInstRef.current.getDate().getFullYear(), 
        calendarInstRef.current.getDate().getMonth(),
        calendarInstRef.current.getDate().getDate().getDate()
      ])
      return currentDate.format(format)
    }

    function setRenderRangeText(){
      const viewName = calendarInstRef.current.getViewName()
      const calDate = calendarInstRef.current.getDate()
      const customMonth = dayjs(calDate).format('MMMM').charAt(0).toUpperCase() + dayjs(calDate).format('MMMM').slice(1)
      const dateRangeText = []

      switch(viewName){
        case "day":
          dateRangeText.push(currentCalendarDate("DD MMMM YYYY"))
          break;
        case "month":
          dateRangeText.push(customMonth)
          dateRangeText.push(currentCalendarDate("YYYY"))
          break;
        default:
          const rangeStart = calendarInstRef.current.getDateRangeStart().getTime()
          const rangeEnd = calendarInstRef.current.getDateRangeEnd().getTime()
          if( dayjs(rangeStart).format("MMMM")=== dayjs(rangeEnd).format("MMMM")) {
            dateRangeText.push(customMonth)
            dateRangeText.push(currentCalendarDate("YYYY"))
          } else {
            dateRangeText.push(customMonth)
            dateRangeText.push("-")
            dateRangeText.push(dayjs(rangeEnd.format("MMM YYYY")))

          }

      }

      setRenderRange(dateRangeText.join(" "))
    }



  }
 
)