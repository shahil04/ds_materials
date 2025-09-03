import React, { Fragment } from 'react'

import { Helmet } from 'react-helmet'

import Navbar8 from '../components/navbar8'
import Hero17 from '../components/hero17'
import Features24 from '../components/features24'
import CTA26 from '../components/cta26'
import Features25 from '../components/features25'
import Pricing14 from '../components/pricing14'
import Steps2 from '../components/steps2'
import Testimonial17 from '../components/testimonial17'
import Contact10 from '../components/contact10'
import Footer4 from '../components/footer4'
import './home.css'

const Home = (props) => {
  return (
    <div className="home-container">
      <Helmet>
        <title>Well Informed Everlasting Kingfisher</title>
        <meta
          property="og:title"
          content="Well Informed Everlasting Kingfisher"
        />
      </Helmet>
      <Navbar8
        page4Description={
          <Fragment>
            <span className="home-text100">
              Access additional resources to enhance your learning experience
            </span>
          </Fragment>
        }
        action1={
          <Fragment>
            <span className="home-text101">Login</span>
          </Fragment>
        }
        link2={
          <Fragment>
            <span className="home-text102">#courses</span>
          </Fragment>
        }
        page1={
          <Fragment>
            <span className="home-text103">Home</span>
          </Fragment>
        }
        link1={
          <Fragment>
            <span className="home-text104">#home</span>
          </Fragment>
        }
        page4={
          <Fragment>
            <span className="home-text105">Resources</span>
          </Fragment>
        }
        page2={
          <Fragment>
            <span className="home-text106">Courses</span>
          </Fragment>
        }
        link4={
          <Fragment>
            <span className="home-text107">#resources</span>
          </Fragment>
        }
        page1Description={
          <Fragment>
            <span className="home-text108">
              Welcome to our educational platform
            </span>
          </Fragment>
        }
        page2Description={
          <Fragment>
            <span className="home-text109">
              Explore our wide range of courses
            </span>
          </Fragment>
        }
        link3={
          <Fragment>
            <span className="home-text110">#enrollment</span>
          </Fragment>
        }
        page3={
          <Fragment>
            <span className="home-text111">Enrollment</span>
          </Fragment>
        }
        page3Description={
          <Fragment>
            <span className="home-text112">
              Find information on how to enroll in our courses
            </span>
          </Fragment>
        }
        action2={
          <Fragment>
            <span className="home-text113">Sign Up</span>
          </Fragment>
        }
      ></Navbar8>
      <Hero17
        action2={
          <Fragment>
            <span className="home-text114">Learn More</span>
          </Fragment>
        }
        action1={
          <Fragment>
            <span className="home-text115">Enroll Now</span>
          </Fragment>
        }
        heading1={
          <Fragment>
            <span className="home-text116">
              Welcome to Our Educational Platform
            </span>
          </Fragment>
        }
        content1={
          <Fragment>
            <span className="home-text117">
              Empowering students and educators with comprehensive course
              information and resources.
            </span>
          </Fragment>
        }
      ></Hero17>
      <Features24
        feature3Description={
          <Fragment>
            <span className="home-text118">Access to Resources</span>
          </Fragment>
        }
        feature3Title={
          <Fragment>
            <span className="home-text119">Resource Library</span>
          </Fragment>
        }
        feature2Description={
          <Fragment>
            <span className="home-text120">Enrollment Details</span>
          </Fragment>
        }
        feature1Title={
          <Fragment>
            <span className="home-text121">Detailed Course Information</span>
          </Fragment>
        }
        feature1Description={
          <Fragment>
            <span className="home-text122">
              Comprehensive details about courses offered
            </span>
          </Fragment>
        }
        feature2Title={
          <Fragment>
            <span className="home-text123">Easy Enrollment Process</span>
          </Fragment>
        }
      ></Features24>
      <CTA26
        heading1={
          <Fragment>
            <span className="home-text124">
              Ready to enroll in our courses?
            </span>
          </Fragment>
        }
        content1={
          <Fragment>
            <span className="home-text125">
              Explore our wide range of courses and start your educational
              journey today.
            </span>
          </Fragment>
        }
        action1={
          <Fragment>
            <span className="home-text126">Enroll Now</span>
          </Fragment>
        }
      ></CTA26>
      <Features25
        feature3Description={
          <Fragment>
            <span className="home-text127">
              Access to a variety of resources such as study materials, videos,
              and interactive tools to enhance learning.
            </span>
          </Fragment>
        }
        feature1Description={
          <Fragment>
            <span className="home-text128">
              Detailed descriptions of courses offered, including syllabus,
              objectives, and prerequisites.
            </span>
          </Fragment>
        }
        feature2Title={
          <Fragment>
            <span className="home-text129">Easy Enrollment Process</span>
          </Fragment>
        }
        feature1Title={
          <Fragment>
            <span className="home-text130">
              Comprehensive Course Information
            </span>
          </Fragment>
        }
        feature2Description={
          <Fragment>
            <span className="home-text131">
              Simple and straightforward enrollment process with online forms
              and payment options.
            </span>
          </Fragment>
        }
        feature3Title={
          <Fragment>
            <span className="home-text132">Rich Learning Resources</span>
          </Fragment>
        }
      ></Features25>
      <Pricing14
        plan3Price={
          <Fragment>
            <span className="home-text133">$199</span>
          </Fragment>
        }
        plan3Action={
          <Fragment>
            <span className="home-text134">Enroll Now</span>
          </Fragment>
        }
        plan11={
          <Fragment>
            <span className="home-text135">Basic plan</span>
          </Fragment>
        }
        plan1Action={
          <Fragment>
            <span className="home-text136">Enroll Now</span>
          </Fragment>
        }
        plan31={
          <Fragment>
            <span className="home-text137">Enterprise plan</span>
          </Fragment>
        }
        plan3Feature41={
          <Fragment>
            <span className="home-text138">Feature text goes here</span>
          </Fragment>
        }
        plan1Feature2={
          <Fragment>
            <span className="home-text139">Interactive online quizzes</span>
          </Fragment>
        }
        plan2Feature11={
          <Fragment>
            <span className="home-text140">Feature text goes here</span>
          </Fragment>
        }
        plan3Feature51={
          <Fragment>
            <span className="home-text141">Feature text goes here</span>
          </Fragment>
        }
        plan2Feature41={
          <Fragment>
            <span className="home-text142">Feature text goes here</span>
          </Fragment>
        }
        plan2Feature2={
          <Fragment>
            <span className="home-text143">
              Live virtual classroom sessions
            </span>
          </Fragment>
        }
        plan3Feature21={
          <Fragment>
            <span className="home-text144">Feature text goes here</span>
          </Fragment>
        }
        plan2Feature4={
          <Fragment>
            <span className="home-text145">Feature text goes here</span>
          </Fragment>
        }
        plan2Yearly={
          <Fragment>
            <span className="home-text146">or $299 yearly</span>
          </Fragment>
        }
        plan1Action1={
          <Fragment>
            <span className="home-text147">Get started</span>
          </Fragment>
        }
        plan2Action={
          <Fragment>
            <span className="home-text148">Enroll Now</span>
          </Fragment>
        }
        plan3Feature1={
          <Fragment>
            <span className="home-text149">All features of Plan 2</span>
          </Fragment>
        }
        plan2Feature3={
          <Fragment>
            <span className="home-text150">One-on-one tutoring sessions</span>
          </Fragment>
        }
        plan1Price1={
          <Fragment>
            <span className="home-text151">$200/yr</span>
          </Fragment>
        }
        plan2={
          <Fragment>
            <span className="home-text152">Business plan</span>
          </Fragment>
        }
        plan2Feature21={
          <Fragment>
            <span className="home-text153">Feature text goes here</span>
          </Fragment>
        }
        plan2Action1={
          <Fragment>
            <span className="home-text154">Get started</span>
          </Fragment>
        }
        plan3Feature2={
          <Fragment>
            <span className="home-text155">
              Priority support from instructors
            </span>
          </Fragment>
        }
        content1={
          <Fragment>
            <span className="home-text156">
              Choose the perfect plan for you
            </span>
          </Fragment>
        }
        plan2Feature1={
          <Fragment>
            <span className="home-text157">All features of Plan 1</span>
          </Fragment>
        }
        heading1={
          <Fragment>
            <span className="home-text158">Pricing plan</span>
          </Fragment>
        }
        plan3Feature31={
          <Fragment>
            <span className="home-text159">Feature text goes here</span>
          </Fragment>
        }
        plan1={
          <Fragment>
            <span className="home-text160">Basic plan</span>
          </Fragment>
        }
        plan21={
          <Fragment>
            <span className="home-text161">Business plan</span>
          </Fragment>
        }
        plan1Feature11={
          <Fragment>
            <span className="home-text162">Feature text goes here</span>
          </Fragment>
        }
        plan1Feature21={
          <Fragment>
            <span className="home-text163">Feature text goes here</span>
          </Fragment>
        }
        plan3Feature5={
          <Fragment>
            <span className="home-text164">Feature text goes here</span>
          </Fragment>
        }
        plan2Yearly1={
          <Fragment>
            <span className="home-text165">or $29 monthly</span>
          </Fragment>
        }
        plan2Price={
          <Fragment>
            <span className="home-text166">$149</span>
          </Fragment>
        }
        plan3Yearly1={
          <Fragment>
            <span className="home-text167">or $49 monthly</span>
          </Fragment>
        }
        plan2Feature31={
          <Fragment>
            <span className="home-text168">Feature text goes here</span>
          </Fragment>
        }
        plan3Feature11={
          <Fragment>
            <span className="home-text169">Feature text goes here</span>
          </Fragment>
        }
        plan1Yearly1={
          <Fragment>
            <span className="home-text170">or $20 monthly</span>
          </Fragment>
        }
        plan2Price1={
          <Fragment>
            <span className="home-text171">$299/yr</span>
          </Fragment>
        }
        plan3Yearly={
          <Fragment>
            <span className="home-text172">or $499 yearly</span>
          </Fragment>
        }
        plan3Feature4={
          <Fragment>
            <span className="home-text173">Feature text goes here</span>
          </Fragment>
        }
        plan3Price1={
          <Fragment>
            <span className="home-text174">$499/yr</span>
          </Fragment>
        }
        plan1Feature31={
          <Fragment>
            <span className="home-text175">Feature text goes here</span>
          </Fragment>
        }
        plan1Feature3={
          <Fragment>
            <span className="home-text176">Certificate upon completion</span>
          </Fragment>
        }
        plan1Yearly={
          <Fragment>
            <span className="home-text177">or $200 yearly</span>
          </Fragment>
        }
        plan1Feature1={
          <Fragment>
            <span className="home-text178">Access to all course materials</span>
          </Fragment>
        }
        plan3Feature3={
          <Fragment>
            <span className="home-text179">Career counseling sessions</span>
          </Fragment>
        }
        content2={
          <Fragment>
            <span className="home-text180">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit.
              <span
                dangerouslySetInnerHTML={{
                  __html: ' ',
                }}
              />
            </span>
          </Fragment>
        }
        plan3Action1={
          <Fragment>
            <span className="home-text181">Get started</span>
          </Fragment>
        }
        plan1Price={
          <Fragment>
            <span className="home-text182">$99</span>
          </Fragment>
        }
        plan3={
          <Fragment>
            <span className="home-text183">Enterprise plan</span>
          </Fragment>
        }
      ></Pricing14>
      <Steps2
        step1Description={
          <Fragment>
            <span className="home-text184">
              Browse through our wide range of courses to find the perfect fit
              for your educational needs.
            </span>
          </Fragment>
        }
        step3Description={
          <Fragment>
            <span className="home-text185">
              Gain access to a variety of educational resources and materials to
              enhance your learning experience.
            </span>
          </Fragment>
        }
        step2Title={
          <Fragment>
            <span className="home-text186">Enroll in a Course</span>
          </Fragment>
        }
        step2Description={
          <Fragment>
            <span className="home-text187">
              Once you&apos;ve found a course of interest, easily enroll and
              secure your spot in the class.
            </span>
          </Fragment>
        }
        step1Title={
          <Fragment>
            <span className="home-text188">Explore Courses</span>
          </Fragment>
        }
        step3Title={
          <Fragment>
            <span className="home-text189">Access Resources</span>
          </Fragment>
        }
        step4Description={
          <Fragment>
            <span className="home-text190">
              Begin your educational journey and start learning with the
              guidance of our experienced educators.
            </span>
          </Fragment>
        }
        step4Title={
          <Fragment>
            <span className="home-text191">Start Learning</span>
          </Fragment>
        }
      ></Steps2>
      <Testimonial17
        author2Position={
          <Fragment>
            <span className="home-text192">Student</span>
          </Fragment>
        }
        author1Position={
          <Fragment>
            <span className="home-text193">Parent</span>
          </Fragment>
        }
        author1Name={
          <Fragment>
            <span className="home-text194">John Doe</span>
          </Fragment>
        }
        author3Name={
          <Fragment>
            <span className="home-text195">Emily Brown</span>
          </Fragment>
        }
        review2={
          <Fragment>
            <span className="home-text196">
              Best decision I made for my academics!
            </span>
          </Fragment>
        }
        author2Name={
          <Fragment>
            <span className="home-text197">Jane Smith</span>
          </Fragment>
        }
        author4Position={
          <Fragment>
            <span className="home-text198">Principal</span>
          </Fragment>
        }
        author4Name={
          <Fragment>
            <span className="home-text199">David Johnson</span>
          </Fragment>
        }
        content1={
          <Fragment>
            <span className="home-text200">
              My child has been attending courses at this institution for a year
              now, and I have seen a significant improvement in their grades and
              confidence. The teachers are dedicated and provide personalized
              attention to each student.
            </span>
          </Fragment>
        }
        author3Position={
          <Fragment>
            <span className="home-text201">Teacher</span>
          </Fragment>
        }
        review1={
          <Fragment>
            <span className="home-text202">
              Excellent institution with great teachers!
            </span>
          </Fragment>
        }
        heading1={
          <Fragment>
            <span className="home-text203">Testimonials</span>
          </Fragment>
        }
        review3={
          <Fragment>
            <span className="home-text204">
              A nurturing environment for both students and teachers.
            </span>
          </Fragment>
        }
        review4={
          <Fragment>
            <span className="home-text205">
              A place where students thrive academically and personally.
            </span>
          </Fragment>
        }
      ></Testimonial17>
      <Contact10
        content1={
          <Fragment>
            <span className="home-text206">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit.
              Suspendisse varius enim in ero.
            </span>
          </Fragment>
        }
        location1Description={
          <Fragment>
            <span className="home-text207">
              123 University Ave, Cityville, State, ZIP
            </span>
          </Fragment>
        }
        heading1={
          <Fragment>
            <span className="home-text208">Contact Us</span>
          </Fragment>
        }
        location2Description={
          <Fragment>
            <span className="home-text209">
              Virtual learning environment accessible worldwide
            </span>
          </Fragment>
        }
        location1={
          <Fragment>
            <span className="home-text210">Main Campus</span>
          </Fragment>
        }
        location2={
          <Fragment>
            <span className="home-text211">Online Campus</span>
          </Fragment>
        }
      ></Contact10>
      <Footer4
        link5={
          <Fragment>
            <span className="home-text212">Contact Us</span>
          </Fragment>
        }
        link3={
          <Fragment>
            <span className="home-text213">Enrollment</span>
          </Fragment>
        }
        link1={
          <Fragment>
            <span className="home-text214">About Us</span>
          </Fragment>
        }
        termsLink={
          <Fragment>
            <span className="home-text215">Terms and Conditions</span>
          </Fragment>
        }
        link2={
          <Fragment>
            <span className="home-text216">Courses</span>
          </Fragment>
        }
        link4={
          <Fragment>
            <span className="home-text217">Resources</span>
          </Fragment>
        }
        cookiesLink={
          <Fragment>
            <span className="home-text218">Cookies Policy</span>
          </Fragment>
        }
        privacyLink={
          <Fragment>
            <span className="home-text219">Privacy Policy</span>
          </Fragment>
        }
      ></Footer4>
    </div>
  )
}

export default Home
