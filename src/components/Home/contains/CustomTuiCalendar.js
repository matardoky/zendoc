import React, {
  useRef,
  useLayoutEffect,
  useEffect,
  forwardRef,
  useImperativeHandle,
  useState
} from 'react'

import TuiCalendar from "tui-calendar"

const CustomTuiCalendar = forwardRef(
  (
    {
      height = "800px",
      defaultView = "week",
      calendars = [],
      schedules = [], 
      isReadOnly = true,
      showSlidebar = false,
      showMenu = false,
      onCreate, 
      createText = "New schedule",
      onBeforeCreateSchedule = () => false,
      onBeforeUpdateSchedule = () => false,
      ...rest
    },
    ref
  ) => {
      const calendarInstRef = useRef(null)
      const tuiRef = useRef(null)
      const wrapperRef = useRef(null)
      const [open, setOpen] = useState(false)
      const [renderRange, setRenderRange] = useState("")
      const [workweek, setWorkweek] = useState(true)
      const [narrowWeekend, setNarrowWeekend] = useState(true)
      const [startDayOfWeek, setStartDayOfWeek] = useState(1)
      const [type, setType] = useState("weekly")
      const [checkedCalendars,setCheckedCalendars ] = useState(
          calendars.map((element) => ({...element, isChecked:true}))
      )
      const [filterSchedules, setFilterSchedules] = useState(schedules)
 
    useImperativeHandle(ref, ()=> ({
        getAlert(){
            alert("getAlert from child")
        }, 
        createSchedule, 
        updateSchedule,
        deleteSchedule
    }))
 
    useEffect(()=>{
      calendarInstRef.current = new TuiCalendar(tuiRef.current, {
        useDetailPopup:false, 
        useCreationPopup:false, 
        template:{
            timegridDisplayPrimayTime: function (time) {
              return (time.hour < 10 ? '0' : '') + time.hour + ':' + time.minutes + '0';
            },
            timegridDisplayTime: function (time) {
              return (time.hour < 10 ? '0' : '') + time.hour + ':' + time.minutes + '0';
            },
        },
        calendars,
        ...rest
      })

      
    })

  }
)
